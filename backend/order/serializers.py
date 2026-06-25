from rest_framework import serializers
from .models import Order, OrderItem, LoyaltySettings, Menu, Category
import math

class MenuSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_name = serializers.CharField(source='category.name', read_only=True)

    # Write-only untuk upload
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    # Read-only URL gambar
    image_url = serializers.SerializerMethodField(read_only=True)

    # Harga web = harga POS + 1% (dibulatkan ke atas ke kelipatan 100)
    web_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Menu
        fields = [
            "id",
            "name",
            "price",        # harga POS (normal)
            "web_price",    # harga web (markup 1%)
            "category",
            "category_name",
            "description",
            "image",
            "image_url",
            "is_available",
            "is_active",
        ]

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_web_price(self, obj):
        if obj.price:
            # Markup 1%, bulatkan ke atas ke kelipatan 500
            marked_up = float(obj.price) * 1.01
            rounded   = math.ceil(marked_up / 500) * 500
            return int(rounded)
        return None


class OrderItemSerializer(serializers.ModelSerializer):
    menu_name = serializers.CharField(source="menu.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "menu_name", "quantity", "price", "notes"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    created_time = serializers.SerializerMethodField()

    def get_created_time(self, obj):
        return obj.created_at.strftime("%H:%M WIB")

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "source",
            "status",
            "payment_status",
            "payment_method",
            "is_deferred_payment",
            "customer_name",
            "customer_phone",
            "table_number",
            "subtotal",
            "discount_amount",
            "total_price",
            "notes",
            "created_at",
            "created_time",
            "items",
        ]


class LoyaltySettingsSerializer(serializers.ModelSerializer):
    # Alias: SystemSettings.vue mengirim/membaca discount_percent,
    # sedangkan model menyimpan discount_percentage.
    # Kedua field di-expose agar keduanya bisa dipakai.
    discount_percent = serializers.DecimalField(
        max_digits=5, decimal_places=2,
        source='discount_percentage',
        required=False,
    )

    class Meta:
        model = LoyaltySettings
        fields = [
            "min_orders",
            "min_spending",
            "period_days",
            "discount_percentage",   # dipakai backend & LoyalCustomers.vue
            "discount_percent",      # alias untuk SystemSettings.vue
            "updated_at",
        ]
        read_only_fields = ["updated_at"]