from django.contrib import admin
from .models import Customer, Order, OrderItem, LoyaltySetting

# 1. Inline OrderItem untuk menampilkan item langsung di dalam form Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('menu', 'quantity', 'price')
    can_delete = False

# 2. Pengaturan Admin untuk Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'final_price', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('customer__phone',)
    readonly_fields = ('created_at',)
    inlines = [OrderItemInline]

# 3. Pengaturan Admin untuk OrderItem (Daftar utama item)
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_order_id', 'menu', 'quantity', 'price')
    list_filter = ('menu__name',)
    
    def get_order_id(self, obj):
        return f"Order #{obj.order.id}"
    get_order_id.short_description = 'Order ID'

# 4. Pengaturan Admin untuk Customer
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('phone', 'name', 'total_orders', 'total_spent')
    search_fields = ('phone', 'name')

# 5. Pengaturan Admin untuk LoyaltySetting
@admin.register(LoyaltySetting)
class LoyaltySettingAdmin(admin.ModelAdmin):
    list_display = ('admin_wa_receiver', 'min_orders_requirement', 'discount_percentage')
    
    # Mencegah penambahan banyak record, hanya boleh satu pengaturan (singleton)
    def has_add_permission(self, request):
        if LoyaltySetting.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False