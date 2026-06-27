"""
orders/views.py
===============
Semua view untuk modul Orders:
  - CRUD Order
  - Loyalty (publik & admin)
  - Reports & Dashboard
  - Export Excel & PDF (menggunakan finance_excel.py & finance_pdf.py)
  - Unpaid Orders & History
"""

from django.db import transaction, models
from django.db.models import Count, Sum, Max
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from decimal import Decimal
from django.db.models import Q
import math
import calendar
import datetime
from datetime import timedelta

# Finance app
from finance.models import Expense

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, OrderItem, CustomerLoyalty, LoyaltySettings, PAYMENT_METHOD_CHOICES
from menu.models import Menu
from .serializers import OrderSerializer, LoyaltySettingsSerializer


# ─────────────────────────────────────────────
# ORDERS — CRUD
# ─────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
@transaction.atomic
def create_order(request):
    data       = request.data
    items_data = data.get('items', [])

    if not items_data:
        return Response({"error": "Items kosong"}, status=400)

    customer_data = data.get('customer') or {}
    phone = (customer_data.get('phone') or data.get('customer_phone', '')).strip()
    name  = (customer_data.get('name')  or data.get('customer_name',  '')).strip()

    source         = data.get('source', 'pos')
    payment_method = data.get('payment_method', 'cash')
    table_number   = data.get('table_number')
    notes          = data.get('notes', '')

    amount_paid = Decimal(str(data.get('amount_paid', 0) or 0))
    kasir_name  = data.get('kasir_name', '').strip()

    raw_payment_status = data.get('payment_status', '')

    # Logika payment_status
    is_qris = payment_method in ('qris', 'qris_manual', 'gateway')

    if source == 'web':
        if is_qris:
            # Web + QRIS → langsung paid & completed
            payment_status = 'paid'
            is_deferred    = False
            order_status   = 'completed'
        else:
            # Web + cash → pending seperti biasa
            payment_status = 'pending'
            is_deferred    = False
            order_status   = 'pending'
    elif raw_payment_status == 'pending' and not is_qris:
        # POS "Makan Dulu" — hanya boleh cash
        payment_status = 'unpaid'
        is_deferred    = True
        order_status   = 'pending'
    else:
        # POS bayar sekarang (cash atau qris)
        payment_status = 'paid'
        is_deferred    = False
        order_status   = 'completed'

    # Kumpulkan & validasi semua item terlebih dahulu
    processed_items = []
    for item_data in items_data:
        menu_obj = get_object_or_404(Menu, id=item_data.get('menu_id'))
        if not menu_obj.is_available:
            return Response(
                {"error": f"Menu '{menu_obj.name}' tidak tersedia"},
                status=400,
            )

        if source == 'web':
            price = item_data.get('price') or menu_obj.price_web
        else:
            price = item_data.get('price') or menu_obj.price

        processed_items.append({
            "menu":  menu_obj,
            "qty":   int(item_data.get('quantity', 1)),
            "price": price,
            "notes": item_data.get('notes', ''),
        })

    # Buat order setelah semua item tervalidasi
    order = Order.objects.create(
        source=source,
        status=order_status,
        payment_status=payment_status,
        payment_method=payment_method,
        is_deferred_payment=is_deferred,
        customer_name=name,
        customer_phone=phone,
        table_number=table_number,
        notes=notes,
        amount_paid=amount_paid,
        kasir_name=kasir_name,
    )

    OrderItem.objects.bulk_create([
        OrderItem(
            order    = order,
            menu     = item["menu"],
            quantity = item["qty"],
            price    = item["price"],
            notes    = item["notes"],
        )
        for item in processed_items
    ])

    order.recalculate_totals()
    if phone:
        order.apply_loyalty_discount()

    order.refresh_from_db()

    if payment_status == "paid" and amount_paid > 0:
        order.change_amount = max(
            amount_paid - order.total_price,
            Decimal("0"),
        )
        order.save(update_fields=["change_amount"])
        order.refresh_from_db()

    return Response(OrderSerializer(order).data, status=201)


@api_view(["GET"])
@permission_classes([AllowAny])
def list_orders(request):
    orders = (
        Order.objects
        .prefetch_related("items__menu")
        .order_by("-created_at")
    )
    return Response(OrderSerializer(orders, many=True).data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_order(request, pk):
    order = get_object_or_404(
        Order.objects.prefetch_related("items__menu"),
        pk=pk,
    )
    return Response(OrderSerializer(order).data)


@api_view(["GET"])
@permission_classes([AllowAny])
def active_orders_per_day(request):
    target_date = request.query_params.get("target_date")
    if not target_date:
        return Response({"error": "Parameter target_date wajib diisi"}, status=400)

    orders = (
        Order.objects
        .filter(created_at__date=target_date)
        .prefetch_related("items__menu")
        .order_by("-created_at")
    )
    return Response(OrderSerializer(orders, many=True).data)


# ─────────────────────────────────────────────
# LOYALTY — PUBLIK
# ─────────────────────────────────────────────

@api_view(["GET"])
@permission_classes([AllowAny])
def check_loyalty_status(request):
    """
    GET /api/orders/check_loyalty_status/?phone=08xxx

    Response:
      - is_loyal          → dipakai semua Vue component
      - discount_percent  → dipakai Cart.vue (POS) & Checkout.vue (web)
      - discount_percentage → alias, nilai sama
    """
    phone = request.query_params.get("phone", "").strip()
    if not phone:
        return Response({
            "is_loyal":            False,
            "discount_percent":    0,
            "discount_percentage": 0,
        })

    # Cek override manual dari admin
    loyalty_override = CustomerLoyalty.objects.filter(
        phone=phone,
        special_discount_percentage__isnull=False,
    ).first()

    if loyalty_override:
        pct = float(loyalty_override.special_discount_percentage)
        return Response({
            "is_loyal":            True,
            "discount_percent":    pct,
            "discount_percentage": pct,
        })

    # Hitung berdasarkan aturan umum
    settings = LoyaltySettings.get_settings()
    cutoff   = timezone.now() - timedelta(days=settings.period_days)
    stats    = Order.objects.filter(
        customer_phone=phone,
        status='completed',
        created_at__gte=cutoff,
    ).aggregate(jumlah=Count('id'), total=Sum('total_price'))

    is_loyal = (
        (stats['jumlah'] or 0) >= settings.min_orders
        and (stats['total'] or Decimal('0')) >= settings.min_spending
    )

    pct = float(settings.discount_percentage) if is_loyal else 0
    return Response({
        "is_loyal":            is_loyal,
        "discount_percent":    pct,
        "discount_percentage": pct,
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def loyal_customers(request):
    settings = LoyaltySettings.get_settings()
    cutoff   = timezone.now() - timedelta(days=settings.period_days)

    aggregated = (
        Order.objects
        .filter(status='completed', created_at__gte=cutoff)
        .exclude(customer_phone='')
        .values('customer_phone')
        .annotate(
            order_count = Count('id'),
            total_spent = Sum('total_price'),
            last_name   = Max('customer_name'),
        )
        .order_by('-total_spent')
    )

    data = []
    for row in aggregated:
        is_loyal = (
            row['order_count'] >= settings.min_orders
            and row['total_spent'] >= settings.min_spending
        )
        data.append({
            "phone":       row['customer_phone'],
            "name":        row['last_name'] or '',
            "order_count": row['order_count'],
            "total_spent": row['total_spent'],
            "is_loyal":    is_loyal,
        })

    return Response(data)


# ─────────────────────────────────────────────
# REPORTS & DASHBOARD
# ─────────────────────────────────────────────

@api_view(["GET"])
@permission_classes([AllowAny])
def order_reports(request):
    month = request.query_params.get("month")
    year  = request.query_params.get("year")

    qs = Order.objects.all()
    if month and year:
        qs = qs.filter(created_at__month=month, created_at__year=year)
    elif year:
        qs = qs.filter(created_at__year=year)

    top_menus = (
        OrderItem.objects.filter(order__in=qs)
        .values("menu__name")
        .annotate(total_qty=Sum("quantity"))
        .order_by("-total_qty")[:5]
    )

    return Response({
        "total_orders":  qs.count(),
        "total_revenue": qs.aggregate(total=Sum("total_price"))["total"] or 0,
        "top_menus":     list(top_menus),
    })


class DashboardStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        date_from = request.query_params.get('date_from')
        date_to   = request.query_params.get('date_to')

        paid_qs = Order.objects.filter(
            payment_status='paid',
        ).exclude(status='cancelled')

        if date_from:
            paid_qs = paid_qs.filter(created_at__date__gte=date_from)
        if date_to:
            paid_qs = paid_qs.filter(created_at__date__lte=date_to)

        paid_stats = paid_qs.aggregate(
            total_revenue=Sum("total_price"),
            total_orders=Count("id"),
        )

        all_qs = Order.objects.all()
        if date_from:
            all_qs = all_qs.filter(created_at__date__gte=date_from)
        if date_to:
            all_qs = all_qs.filter(created_at__date__lte=date_to)

        pending   = all_qs.filter(status="pending").count()
        completed = all_qs.filter(status="completed").count()

        top_menu_qs = OrderItem.objects.filter(
            order__payment_status='paid',
        ).exclude(order__status='cancelled')

        if date_from:
            top_menu_qs = top_menu_qs.filter(order__created_at__date__gte=date_from)
        if date_to:
            top_menu_qs = top_menu_qs.filter(order__created_at__date__lte=date_to)

        top_menus = (
            top_menu_qs
            .values("menu__name")
            .annotate(
                total_qty=Sum("quantity"),
                total_revenue=Sum(
                    models.ExpressionWrapper(
                        models.F("price") * models.F("quantity"),
                        output_field=models.DecimalField(),
                    )
                ),
            )
            .order_by("-total_qty")[:5]
        )

        # Loyal users — selalu berdasarkan period_days, tidak ikut filter tanggal
        settings_obj = LoyaltySettings.get_settings()
        cutoff       = timezone.now() - timedelta(days=settings_obj.period_days)
        loyal_count  = (
            Order.objects
            .filter(status='completed', created_at__gte=cutoff)
            .exclude(customer_phone='')
            .values('customer_phone')
            .annotate(jumlah=Count('id'), total=Sum('total_price'))
            .filter(
                jumlah__gte=settings_obj.min_orders,
                total__gte=settings_obj.min_spending,
            )
            .count()
        )

        return Response({
            "total_revenue":    paid_stats["total_revenue"] or 0,
            "total_orders":     paid_stats["total_orders"]  or 0,
            "pending_orders":   pending,
            "completed_orders": completed,
            "top_menus": [
                {
                    "name":          m["menu__name"],
                    "total_qty":     m["total_qty"],
                    "total_revenue": m["total_revenue"] or 0,
                }
                for m in top_menus
            ],
            "loyal_users": loyal_count,
        })


@api_view(["GET"])
@permission_classes([AllowAny])
def admin_dashboard_daily_stats(request):
    target_date = request.query_params.get("target_date")

    revenue        = 0
    expenses_total = 0

    if target_date:
        revenue = Order.objects.filter(
            created_at__date=target_date,
            payment_status='paid',
        ).exclude(status='cancelled').aggregate(
            total=Sum("total_price")
        )["total"] or 0

        expenses_total = Expense.objects.filter(
            date=target_date
        ).aggregate(total=Sum("amount"))["total"] or 0

    return Response({
        "revenue":    revenue,
        "expenses":   expenses_total,
        "net_profit": revenue - expenses_total,
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def finance_monthly_summary(request):
    from django.db.models.functions import TruncMonth, ExtractMonth

    year = int(request.query_params.get("year", timezone.now().year))

    revenue_qs = (
        Order.objects
        .filter(created_at__year=year, payment_status='paid')
        .exclude(status='cancelled')
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('total_price'))
        .order_by('month')
    )
    revenue_map = {r['month'].month: r['total'] for r in revenue_qs}

    expense_qs = (
        Expense.objects
        .filter(date__year=year)
        .annotate(month_num=ExtractMonth('date'))
        .values('month_num')
        .annotate(total=Sum('amount'))
    )
    expense_map = {e['month_num']: e['total'] for e in expense_qs}

    result = []
    for m in range(1, 13):
        rev = revenue_map.get(m, 0)
        exp = expense_map.get(m, 0)
        result.append({
            "month":      m,
            "month_name": calendar.month_name[m],
            "revenue":    rev,
            "expenses":   exp,
            "net_profit": rev - exp,
        })

    return Response({"year": year, "data": result})


@api_view(["GET"])
@permission_classes([AllowAny])
def finance_daily_summary(request):
    """
    GET /api/orders/finance/daily/?year=2026&month=6
    Mengembalikan pendapatan & pengeluaran per hari dalam satu bulan.
    """
    from django.db.models.functions import TruncDate

    year  = int(request.query_params.get("year",  timezone.now().year))
    month = int(request.query_params.get("month", timezone.now().month))

    revenue_qs = (
        Order.objects
        .filter(
            created_at__year=year,
            created_at__month=month,
            payment_status='paid',
        )
        .exclude(status='cancelled')
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(total=Sum('total_price'))
        .order_by('day')
    )
    revenue_map = {str(r['day']): r['total'] for r in revenue_qs}

    expense_qs = (
        Expense.objects
        .filter(date__year=year, date__month=month)
        .values('date')
        .annotate(total=Sum('amount'))
    )
    expense_map = {str(e['date']): e['total'] for e in expense_qs}

    days_in_month = calendar.monthrange(year, month)[1]
    result = []
    for d in range(1, days_in_month + 1):
        date_str = f"{year}-{month:02d}-{d:02d}"
        rev = revenue_map.get(date_str, 0)
        exp = expense_map.get(date_str, 0)
        result.append({
            "date":       date_str,
            "day":        d,
            "revenue":    rev,
            "expenses":   exp,
            "net_profit": rev - exp,
        })

    return Response({"year": year, "month": month, "data": result})


# ─────────────────────────────────────────────
# EXPORT
# ─────────────────────────────────────────────

@api_view(["GET"])
@permission_classes([AllowAny])
def export_excel_report(request):
    """
    GET /api/orders/export/finance-excel/?mode=monthly&month=7&year=2026
    GET /api/orders/export/finance-excel/?mode=yearly&year=2026
    """
    from .finance_excel import export_finance_excel_view
    return export_finance_excel_view(request)


@api_view(["GET"])
@permission_classes([AllowAny])
def export_pdf_report(request):
    """
    GET /api/orders/export/finance-pdf/?mode=monthly&month=7&year=2026
    GET /api/orders/export/finance-pdf/?mode=yearly&year=2026
    """
    from .finance_pdf import export_finance_pdf_view
    return export_finance_pdf_view(request)


# ─────────────────────────────────────────────
# LOYALTY — ADMIN
# ─────────────────────────────────────────────

class LoyaltySettingsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response(LoyaltySettingsSerializer(LoyaltySettings.get_settings()).data)

    def put(self, request):
        settings   = LoyaltySettings.get_settings()
        serializer = LoyaltySettingsSerializer(settings, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoyalCustomersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        settings = LoyaltySettings.get_settings()
        cutoff   = timezone.now() - timedelta(days=settings.period_days)

        aggregated = (
            Order.objects
            .filter(status='completed', created_at__gte=cutoff)
            .exclude(customer_phone='')
            .values('customer_phone')
            .annotate(
                order_count   = Count('id'),
                total_belanja = Sum('total_price'),
                nama_terakhir = Max('customer_name'),
            )
            .order_by('-total_belanja')
        )

        overrides = {
            cl.phone: cl.special_discount_percentage
            for cl in CustomerLoyalty.objects.exclude(
                special_discount_percentage__isnull=True
            )
        }

        customers = []
        for row in aggregated:
            is_loyal = (
                row['order_count'] >= settings.min_orders
                and row['total_belanja'] >= settings.min_spending
            )
            customers.append({
                "phone":                       row['customer_phone'],
                "name":                        row['nama_terakhir'] or '',
                "order_count":                 row['order_count'],
                "total_spent":                 row['total_belanja'],
                "status":                      'LOYAL MEMBER' if is_loyal else 'REGULAR',
                "is_loyal":                    is_loyal,
                "special_discount_percentage": overrides.get(row['customer_phone']),
            })

        return Response({
            "settings":  LoyaltySettingsSerializer(settings).data,
            "customers": customers,
        })


class GiveSpecialPriceView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, phone):
        discount = request.data.get('discount_percentage')
        if discount is None:
            return Response({'detail': 'discount_percentage wajib diisi'}, status=400)

        loyalty, _ = CustomerLoyalty.objects.get_or_create(
            phone=phone,
            defaults={'name': request.data.get('name', '')},
        )
        loyalty.special_discount_percentage = Decimal(str(discount))
        loyalty.save(update_fields=['special_discount_percentage', 'updated_at'])

        return Response({
            'phone':                       phone,
            'special_discount_percentage': float(loyalty.special_discount_percentage),
        })

    def delete(self, request, phone):
        CustomerLoyalty.objects.filter(phone=phone).update(
            special_discount_percentage=None
        )
        return Response(status=204)


# ─────────────────────────────────────────────
# UNPAID ORDERS & HISTORY
# ─────────────────────────────────────────────

@api_view(["GET"])
@permission_classes([AllowAny])
def unpaid_orders(request):
    search = request.query_params.get("search", "")

    qs = (
        Order.objects
        .filter(payment_status__in=["unpaid", "pending"])
        .prefetch_related("items__menu")
    )

    if search:
        qs = qs.filter(
            Q(customer_name__icontains=search)
            | Q(customer_phone__icontains=search)
            | Q(order_number__icontains=search)
        )

    return Response(
        OrderSerializer(qs.order_by("-created_at"), many=True).data
    )


@api_view(["PATCH"])
@permission_classes([AllowAny])
def pay_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    previous_status = order.status

    amount_paid = Decimal(str(request.data.get('amount_paid', 0) or 0))
    kasir_name  = request.data.get('kasir_name', '').strip()

    order.payment_status = "paid"
    order.status         = "completed"
    order.payment_method = (
        request.data.get("payment_method") or order.payment_method or "cash"
    )
    order.kasir_name     = kasir_name or order.kasir_name
    order.amount_paid    = amount_paid

    if amount_paid > 0:
        order.change_amount = max(amount_paid - order.total_price, Decimal('0'))

    order._previous_status = previous_status
    order.save()
    order.refresh_from_db()

    return Response({
        "success":       True,
        "order_number":  order.order_number,
        "change_amount": float(order.change_amount),
        "amount_paid":   float(order.amount_paid),
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def order_history(request):
    """
    GET /api/orders/history/?period=today|week|month
    GET /api/orders/history/?period=month&year=2026&month=6
    """
    period = request.query_params.get("period", "today")
    now    = timezone.now()

    qs = Order.objects.prefetch_related("items__menu")

    if period == "today":
        qs = qs.filter(created_at__date=now.date())

    elif period == "week":
        qs = qs.filter(created_at__gte=now - timedelta(days=7))

    elif period == "month":
        year  = request.query_params.get("year",  now.year)
        month = request.query_params.get("month", now.month)
        qs    = qs.filter(
            created_at__year=int(year),
            created_at__month=int(month),
        )

    elif period == "year":
        year = request.query_params.get("year", now.year)
        qs   = qs.filter(created_at__year=int(year))

    return Response(
        OrderSerializer(qs.order_by("-created_at"), many=True).data
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def order_full_report(request):
    from django.db.models.functions import ExtractHour, TruncDate, TruncMonth

    period = request.query_params.get("period", "lifetime")
    now    = timezone.now()
    year   = int(request.query_params.get("year",  now.year))
    month  = int(request.query_params.get("month", now.month))
    days   = int(request.query_params.get("days",  7))
    offset = int(request.query_params.get("offset", 0))

    if days not in (7, 14, 28, 30):
        days = 7

    # ── 1. Tentukan period_start / period_end ──────────────────────────
    period_start = None
    period_end   = None

    if period == "week":
        period_end   = now.date() - timedelta(days=offset)
        period_start = period_end - timedelta(days=days - 1)

    elif period == "month":
        period_start = datetime.date(year, month, 1)
        period_end   = datetime.date(year, month, calendar.monthrange(year, month)[1])

    elif period == "year":
        period_start = datetime.date(year, 1, 1)
        period_end   = datetime.date(year, 12, 31)

    # ── 2. Base queryset ───────────────────────────────────────────────
    qualifying_qs = Order.objects.filter(payment_status="paid").exclude(status="cancelled")
    if period_start and period_end:
        qualifying_qs = qualifying_qs.filter(
            created_at__date__gte=period_start,
            created_at__date__lte=period_end,
        )

    qualifying_ids = list(qualifying_qs.values_list("id", flat=True))

    # ── 3. Stats utama ─────────────────────────────────────────────────
    main_stats = qualifying_qs.aggregate(
        total_omzet=Sum("total_price"),
        total_transaksi=Count("id"),
    )
    total_omzet     = main_stats["total_omzet"] or 0
    total_transaksi = main_stats["total_transaksi"] or 0
    rata_rata       = (total_omzet / total_transaksi) if total_transaksi else 0
    menu_aktif      = Menu.objects.filter(is_active=True).count()

    # ── 4. Trend ───────────────────────────────────────────────────────
    base_trend_qs = (
        Order.objects.filter(payment_status="paid").exclude(status="cancelled")
    )

    if period == "year":
        BULAN_ID = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"]
        trend_qs = (
            base_trend_qs
            .filter(created_at__date__gte=period_start, created_at__date__lte=period_end)
            .annotate(period_label=TruncMonth("created_at"))
            .values("period_label")
            .annotate(omzet=Sum("total_price"), transaksi=Count("id"))
            .order_by("period_label")
        )
        trend_labels    = [BULAN_ID[t["period_label"].month - 1] for t in trend_qs]
        trend_dates     = [str(t["period_label"].date()) for t in trend_qs]
        trend_omzet     = [float(t["omzet"] or 0) for t in trend_qs]
        trend_transaksi = [t["transaksi"] for t in trend_qs]

    elif period in ("week", "month") and period_start and period_end:
        trend_qs = (
            base_trend_qs
            .filter(created_at__date__gte=period_start, created_at__date__lte=period_end)
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(omzet=Sum("total_price"), transaksi=Count("id"))
        )
        trend_map = {}
        for row in trend_qs:
            d = row["day"]
            if hasattr(d, "date"):
                d = d.date()
            trend_map[d] = row

        HARI_ID = ["Sen","Sel","Rab","Kam","Jum","Sab","Min"]
        trend_labels, trend_dates, trend_omzet, trend_transaksi = [], [], [], []
        for i in range((period_end - period_start).days + 1):
            d   = period_start + timedelta(days=i)
            row = trend_map.get(d)
            trend_labels.append(HARI_ID[d.weekday()])
            trend_dates.append(str(d))
            trend_omzet.append(float(row["omzet"]) if row else 0)
            trend_transaksi.append(row["transaksi"] if row else 0)

    else:
        # Lifetime — by date
        trend_qs = (
            base_trend_qs
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(omzet=Sum("total_price"), transaksi=Count("id"))
            .order_by("day")
        )
        trend_labels    = [str(t["day"]) for t in trend_qs]
        trend_dates     = trend_labels[:]
        trend_omzet     = [float(t["omzet"] or 0) for t in trend_qs]
        trend_transaksi = [t["transaksi"] for t in trend_qs]

    # ── 5. Top menu ────────────────────────────────────────────────────
    base_item_qs = OrderItem.objects.filter(order_id__in=qualifying_ids)

    top_by_qty = list(
        base_item_qs.values("menu__name")
        .annotate(
            qty=Sum("quantity"),
            omzet=Sum(
                models.ExpressionWrapper(
                    models.F("price") * models.F("quantity"),
                    output_field=models.DecimalField(),
                )
            ),
        )
        .order_by("-qty")[:10]
    )
    top_by_omzet = list(
        base_item_qs.values("menu__name")
        .annotate(
            omzet=Sum(
                models.ExpressionWrapper(
                    models.F("price") * models.F("quantity"),
                    output_field=models.DecimalField(),
                )
            ),
        )
        .order_by("-omzet")[:5]
    )

    # ── 6. Menu tidak laku ─────────────────────────────────────────────
    menu_tidak_laku = list(
        Menu.objects.filter(is_active=True)
        .annotate(
            transaksi=Count("orderitem", filter=Q(orderitem__order_id__in=qualifying_ids))
        )
        .order_by("transaksi", "name")
        .values("name", "transaksi")[:10]
    )

    # ── 7. Metode pembayaran ───────────────────────────────────────────
    pembayaran_qs = (
        qualifying_qs.values("payment_method")
        .annotate(count=Count("id"), total=Sum("total_price"))
        .order_by("-total")
    )
    method_labels         = dict(PAYMENT_METHOD_CHOICES)
    total_revenue_for_pct = float(total_omzet) or 1
    metode_pembayaran = [
        {
            "method":  row["payment_method"],
            "label":   method_labels.get(row["payment_method"], row["payment_method"] or "Lainnya"),
            "count":   row["count"],
            "total":   float(row["total"] or 0),
            "percent": round(float(row["total"] or 0) / total_revenue_for_pct * 100, 1),
        }
        for row in pembayaran_qs
    ]

    # ── 8. Pelanggan ───────────────────────────────────────────────────
    first_order_map = {
        row["customer_phone"]: row["first_date"]
        for row in (
            Order.objects.filter(payment_status="paid")
            .exclude(status="cancelled")
            .exclude(customer_phone="")
            .values("customer_phone")
            .annotate(first_date=models.Min("created_at"))
        )
    }
    phones_in_period = (
        qualifying_qs.exclude(customer_phone="")
        .values_list("customer_phone", flat=True)
        .distinct()
    )
    pelanggan_baru = 0
    pelanggan_lama = 0
    for phone in phones_in_period:
        first_date = first_order_map.get(phone)
        if not first_date:
            continue
        if period_start and first_date.date() < period_start:
            pelanggan_lama += 1
        else:
            pelanggan_baru += 1

    settings_obj    = LoyaltySettings.get_settings()
    loyal_overrides = set(
        CustomerLoyalty.objects.exclude(special_discount_percentage__isnull=True)
        .values_list("phone", flat=True)
    )
    per_phone_stats = (
        qualifying_qs.exclude(customer_phone="")
        .values("customer_phone")
        .annotate(jumlah=Count("id"), total=Sum("total_price"))
    )
    member_loyal = 0
    for row in per_phone_stats:
        if row["customer_phone"] in loyal_overrides:
            member_loyal += 1
            continue
        if (
            row["jumlah"] >= settings_obj.min_orders
            and (row["total"] or Decimal("0")) >= settings_obj.min_spending
        ):
            member_loyal += 1

    # ── 9. Jam teramai ─────────────────────────────────────────────────
    jam_qs = (
        qualifying_qs.annotate(hour=ExtractHour("created_at"))
        .values("hour")
        .annotate(count=Count("id"))
        .order_by("-count")[:5]
    )
    jam_teramai = [
        {
            "hour":  row["hour"],
            "label": f"{row['hour']:02d}.00 - {(row['hour'] + 1) % 24:02d}.00",
            "count": row["count"],
        }
        for row in sorted(jam_qs, key=lambda x: x["hour"])
    ]

    return Response({
        "period": {
            "mode":   period,
            "year":   year,
            "month":  month,
            "days":   days,
            "start":  str(period_start) if period_start else None,
            "end":    str(period_end)   if period_end   else None,
        },
        "stats": {
            "total_omzet":         float(total_omzet),
            "total_transaksi":     total_transaksi,
            "rata_rata_transaksi": float(rata_rata),
            "menu_aktif":          menu_aktif,
        },
        "trend": {
            "labels":    trend_labels,
            "dates":     trend_dates,
            "omzet":     trend_omzet,
            "transaksi": trend_transaksi,
        },
        "top_menu": [
            {"name": r["menu__name"], "qty": r["qty"], "omzet": float(r["omzet"] or 0)}
            for r in top_by_qty
        ],
        "menu_paling_menghasilkan": [
            {"name": r["menu__name"], "omzet": float(r["omzet"] or 0)}
            for r in top_by_omzet
        ],
        "menu_tidak_laku": menu_tidak_laku,
        "metode_pembayaran": metode_pembayaran,
        "pelanggan": {
            "baru":         pelanggan_baru,
            "lama":         pelanggan_lama,
            "loyal_member": member_loyal,
        },
        "jam_teramai": jam_teramai,
    })