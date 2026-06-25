from django.contrib import admin
from .models import (
    Order,
    OrderItem,
    CustomerLoyalty,
    LoyaltySettings,
)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("menu", "quantity", "price")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_number",
        "customer_name",
        "customer_phone",
        "total_price",
        "payment_method",
        "payment_status",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_status",
        "payment_method",
        "source",
    )

    search_fields = (
        "order_number",
        "customer_name",
        "customer_phone",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "menu",
        "quantity",
        "price",
    )

    list_filter = ("menu",)


@admin.register(CustomerLoyalty)
class CustomerLoyaltyAdmin(admin.ModelAdmin):
    list_display = (
        "phone",
        "name",
        "special_discount_percentage",
    )

    search_fields = (
        "phone",
        "name",
    )


@admin.register(LoyaltySettings)
class LoyaltySettingsAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return not LoyaltySettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False