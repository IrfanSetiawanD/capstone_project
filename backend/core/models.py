from django.db import models


# ========================
# USER / CUSTOMER
# ========================
class Customer(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True)
    total_orders = models.IntegerField(default=0)
    total_spent = models.FloatField(default=0)

    def __str__(self):
        return self.phone


# ========================
# CATEGORY
# ========================
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# ========================
# MENU
# ========================
class Menu(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    stock = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# ========================
# ORDER
# ========================
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('diproses', 'Diproses'),
        ('selesai', 'Selesai'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('transfer', 'Transfer'),
        ('wa', 'WhatsApp'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_price = models.FloatField()
    discount = models.FloatField(default=0)
    final_price = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


# ========================
# ORDER ITEM
# ========================
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.menu.name} x {self.quantity}"