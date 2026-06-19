import time
from django.db import transaction
from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import OrderInputSerializer, OrderSerializer 
from .models import Customer, Order, OrderItem, LoyaltySetting
from menu.models import Menu 
from .permissions import IsStaffOrOwner

# --- NEW: Endpoint untuk dicek oleh Frontend di halaman Checkout ---
@api_view(['GET'])
@permission_classes([AllowAny])
def check_loyalty_status(request):
    phone = request.query_params.get('phone', '').strip()
    if not phone:
        return Response({"is_loyal": False, "discount_percent": 0}, status=400)
    
    try:
        customer = Customer.objects.get(phone=phone)
        loyalty = LoyaltySetting.objects.first()
        
        # Cek syarat loyalitas berdasarkan database
        if loyalty and customer.total_orders >= loyalty.min_orders_requirement:
            return Response({
                "is_loyal": True, 
                "discount_percent": loyalty.discount_percentage
            })
        return Response({"is_loyal": False, "discount_percent": 0})
    except Customer.DoesNotExist:
        return Response({"is_loyal": False, "discount_percent": 0})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    serializer = OrderInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    data = serializer.validated_data
    
    with transaction.atomic():
        # 1. Identifikasi Pelanggan
        phone_input = data.get('phone', '').strip()
        if not phone_input:
            generated_phone = f"ANON-{int(time.time())}"
            customer = Customer.objects.create(name="Pelanggan Umum", phone=generated_phone)
        else:
            customer, _ = Customer.objects.get_or_create(phone=phone_input)
            if not customer.name:
                customer.name = f"Customer {phone_input[-4:]}"
                customer.save()

        # 2. Pengecekan Stok & Status Menu
        calculated_total = 0
        order_items_to_create = []
        
        for item in data['items']:
            try:
                menu_obj = Menu.objects.select_for_update().get(pk=item['menu_id'])
                if not menu_obj.is_active:
                    return Response({"error": f"Menu {menu_obj.name} tidak tersedia"}, status=400)
                if menu_obj.stock < item['quantity']:
                    return Response({"error": f"Stok {menu_obj.name} tidak mencukupi"}, status=400)
                
                calculated_total += (menu_obj.price * item['quantity'])
                order_items_to_create.append({
                    'menu_obj': menu_obj, 
                    'qty': item['quantity'], 
                    'price': menu_obj.price
                })
            except Menu.DoesNotExist:
                return Response({"error": f"Menu ID {item['menu_id']} tidak ditemukan"}, status=404)

        # 3. Kalkulasi Diskon (Server-side validation)
        loyalty = LoyaltySetting.objects.first()
        discount_val = 0
        if loyalty and customer.total_orders >= loyalty.min_orders_requirement:
            discount_val = calculated_total * (loyalty.discount_percentage / 100)

        final_price = calculated_total - discount_val

        # 4. Simpan Transaksi
        order = Order.objects.create(
            customer=customer,
            total_price=calculated_total,
            discount=discount_val,
            final_price=final_price,
            payment_method=data['payment_method'],
            status='pending'
        )

        for item in order_items_to_create:
            OrderItem.objects.create(
                order=order, 
                menu=item['menu_obj'], 
                quantity=item['qty'], 
                price=item['price']
            )
            item['menu_obj'].stock -= item['qty']
            item['menu_obj'].save()

        # Update data customer
        customer.total_orders += 1
        customer.total_spent += float(final_price)
        customer.save()

    return Response({
        "message": "Pesanan sukses", 
        "order_id": order.id, 
        "discount": discount_val
    }, status=201)

class DashboardStatsView(APIView):
    permission_classes = [IsStaffOrOwner]

    def get(self, request):
        stats = Order.objects.aggregate(total_rev=Sum('final_price'), total_orders_count=Sum('id'))
        return Response({
            "total_revenue": stats['total_rev'] or 0,
            "total_orders": Order.objects.count(),
            "role_status": f"Logged in as {request.user.profile.role if hasattr(request.user, 'profile') else 'Staff'}"
        })