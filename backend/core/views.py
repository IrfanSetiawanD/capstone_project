from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer, Menu, Order, OrderItem, Category
from .serializers import OrderSerializer
import urllib.parse


# ========================
# DISCOUNT LOGIC
# ========================
def get_discount(total_orders, total_spent):
    if total_orders >= 10 and total_spent >= 100000:
        if total_orders >= 20:
            return 0.15
        return 0.10
    return 0


# ========================
# GET MENU (UNTUK FRONTEND)
# ========================
@api_view(['GET'])
def get_menus(request):
    menus = Menu.objects.filter(is_active=True)

    data = []
    for menu in menus:
        data.append({
            "id": menu.id,
            "name": menu.name,
            "price": menu.price,
            "stock": menu.stock,
            "category": menu.category.name
        })

    return Response(data)


# ========================
# CREATE ORDER (INTI SYSTEM)
# ========================
@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    phone = serializer.validated_data['phone']
    items = serializer.validated_data['items']
    payment_method = serializer.validated_data['payment_method']

    # ========================
    # GET / CREATE CUSTOMER
    # ========================
    customer, created = Customer.objects.get_or_create(phone=phone)

    total_price = 0
    order_items = []

    # ========================
    # HITUNG TOTAL
    # ========================
    for item in items:
        try:
            menu = Menu.objects.get(id=item['menu_id'])
        except Menu.DoesNotExist:
            return Response({"error": "Menu tidak ditemukan"}, status=404)

        if menu.stock < item['quantity']:
            return Response({"error": f"Stock {menu.name} tidak cukup"}, status=400)

        subtotal = menu.price * item['quantity']
        total_price += subtotal

        order_items.append({
            "menu": menu,
            "quantity": item['quantity'],
            "price": menu.price
        })

    # ========================
    # DISKON
    # ========================
    discount_rate = get_discount(customer.total_orders, customer.total_spent)
    discount_amount = total_price * discount_rate
    final_price = total_price - discount_amount

    # ========================
    # CREATE ORDER
    # ========================
    order = Order.objects.create(
        customer=customer,
        total_price=total_price,
        discount=discount_amount,
        final_price=final_price,
        payment_method=payment_method,
        status='pending'
    )

    # ========================
    # CREATE ORDER ITEMS
    # ========================
    for item in order_items:
        OrderItem.objects.create(
            order=order,
            menu=item['menu'],
            quantity=item['quantity'],
            price=item['price']
        )

        # Kurangi stok
        item['menu'].stock -= item['quantity']
        item['menu'].save()

    # ========================
    # UPDATE CUSTOMER
    # ========================
    customer.total_orders += 1
    customer.total_spent += final_price
    customer.save()

    # ========================
    # GENERATE WHATSAPP
    # ========================
    message = "Halo, saya pesan:\n"

    for item in order_items:
        message += f"- {item['menu'].name} x {item['quantity']}\n"

    message += f"\nTotal: Rp {int(final_price)}"

    encoded_message = urllib.parse.quote(message)

    # ⚠️ GANTI NOMOR INI
    wa_link = f"https://wa.me/628123456789?text={encoded_message}"

    return Response({
        "message": "Order berhasil",
        "order_id": order.id,
        "total": final_price,
        "wa_link": wa_link
    })