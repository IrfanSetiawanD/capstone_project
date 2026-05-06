from django.contrib import admin
from .models import Customer, Category, Menu, Order, OrderItem


# ========================
# INLINE ORDER ITEMS
# ========================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('menu', 'quantity', 'price')


# ========================
# ORDER ADMIN
# ========================
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'final_price', 'status', 'created_at')
    inlines = [OrderItemInline]


# ========================
# REGISTER
# ========================
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Menu)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)