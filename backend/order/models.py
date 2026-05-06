from django.db import models

class LoyaltyProfile(models.Model):
    phone_number = models.CharField("Nomor Telepon", max_length=20, unique=True)
    total_orders = models.PositiveIntegerField("Qty Pesanan", default=0)
    total_spent = models.DecimalField("Total Belanja", max_digits=12, decimal_places=0, default=0)
    last_order_date = models.DateTimeField(auto_now=True)
    
    @property
    def status_poin(self):
        return int(self.total_spent / 10000)

    def __str__(self):
        return f"{self.phone_number} - {self.total_orders} Orders"

class OrderHistory(models.Model):
    customer_wa = models.CharField(max_length=20)
    menu_name = models.CharField(max_length=100) 
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_wa} - {self.menu_name}"

# SEJAJARKAN KE KIRI (Jangan di dalam OrderHistory)
class LoyaltySetting(models.Model):
    admin_wa_receiver = models.CharField("WA Admin", max_length=20, default="628xxx")
    min_orders_requirement = models.IntegerField("Min. Pesanan", default=10)
    min_spending_requirement = models.DecimalField("Min. Belanja", max_digits=12, decimal_places=0, default=200000)
    discount_percentage = models.IntegerField("Diskon (%)", default=10)

    def __str__(self):
        return "Pengaturan Loyalitas"