from rest_framework import serializers
from .models import Order, OrderItem, Customer

# ==========================================
# 1. INPUT SERIALIZERS (Digunakan saat checkout/POST)
# ==========================================
class OrderItemInputSerializer(serializers.Serializer):
    menu_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class OrderInputSerializer(serializers.Serializer):
    phone = serializers.CharField(required=False, allow_blank=True)
    payment_method = serializers.CharField()
    order_type = serializers.CharField(required=False, allow_blank=True)
    items = OrderItemInputSerializer(many=True)

# ==========================================
# 2. OUTPUT SERIALIZERS (Digunakan saat GET/List)
# ==========================================
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone']

class OrderItemSerializer(serializers.ModelSerializer):
    # Mengambil nama menu dari relasi model OrderItem -> Menu
    menu_name = serializers.ReadOnlyField(source='menu.name')
    
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    # Serializer bersarang untuk menampilkan data lengkap
    customer = CustomerSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'total_price', 'discount', 
            'final_price', 'status', 'payment_method', 
            'created_at', 'items'
        ]