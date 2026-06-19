# order/models.py
from django.db import models
# Ambil model Menu dari aplikasi menu untuk dihubungkan ke transaksi
from menu.models import Menu 

class Customer(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True)
    total_orders = models.IntegerField(default=0)
    total_spent = models.FloatField(default=0)

    def __str__(self):
        return self.phone


class Order(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('diproses', 'Diproses'), ('selesai', 'Selesai')]
    PAYMENT_CHOICES = [('cash', 'Cash'), ('transfer', 'Transfer'), ('wa', 'WhatsApp'), ('qris', 'QRIS')]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    total_price = models.FloatField()
    discount = models.FloatField(default=0)
    final_price = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE) # <--- Menggunakan model Menu dari aplikasi sebelah
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.menu.name} x {self.quantity}"


class LoyaltySetting(models.Model):
    admin_wa_receiver = models.CharField("WA Admin", max_length=20, default="628xxx")
    min_orders_requirement = models.IntegerField("Min. Pesanan", default=10)
    discount_percentage = models.IntegerField("Diskon (%)", default=10)

    def __str__(self):
        return "Pengaturan Loyalitas"