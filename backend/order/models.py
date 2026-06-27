from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta, datetime
from django.db.models import Count, Sum
import random
import string

from menu.models import Menu


# ─────────────────────────────────────────────
# CHOICES
# ─────────────────────────────────────────────

ORDER_SOURCE_CHOICES = (
    ('web', 'Web'),
    ('pos', 'POS'),
)

ORDER_STATUS_CHOICES = (
    ('pending',    'Pending'),
    ('processing', 'Processing'),
    ('completed',  'Completed'),
    ('cancelled',  'Cancelled'),
)

PAYMENT_STATUS_CHOICES = (
    ('unpaid',  'Unpaid'),
    ('paid',    'Paid'),
    ('pending', 'Pending'),
)

PAYMENT_METHOD_CHOICES = (
    ('cash',        'Cash'),
    ('qris',        'QRIS'),
    ('qris_manual', 'QRIS Manual'),
    ('gateway',     'Payment Gateway'),
)


# ─────────────────────────────────────────────
# ORDER
# ─────────────────────────────────────────────

class Order(models.Model):
    order_number = models.CharField(max_length=30, unique=True, editable=False, blank=True)

    source         = models.CharField(max_length=10, choices=ORDER_SOURCE_CHOICES, default='web')
    status         = models.CharField(max_length=15, choices=ORDER_STATUS_CHOICES, default='pending')

    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    is_deferred_payment = models.BooleanField(
        default=False,
        help_text='POS: pelanggan makan dulu, bayar nanti',
    )

    customer_name  = models.CharField(max_length=100, blank=True)
    customer_phone = models.CharField(max_length=20, blank=True, db_index=True)
    table_number   = models.CharField(max_length=10, blank=True, null=True)

    subtotal        = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    total_price     = models.DecimalField(max_digits=12, decimal_places=0, default=0)

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    amount_paid = models.DecimalField(
    max_digits=12,
    decimal_places=0,
    default=0
    )

    change_amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0
    )

    kasir_name = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_number} [{self.get_source_display()}]"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = generate_order_number()
        super().save(*args, **kwargs)

    def recalculate_totals(self):
        subtotal        = sum((item.subtotal for item in self.items.all()), Decimal('0'))
        self.subtotal   = subtotal
        self.total_price = subtotal - self.discount_amount
        self.save(update_fields=['subtotal', 'total_price'])

    def apply_loyalty_discount(self):
        if not self.customer_phone:
            return

        loyalty = CustomerLoyalty.objects.filter(phone=self.customer_phone).first()
        if loyalty and loyalty.special_discount_percentage is not None:
            rate = loyalty.special_discount_percentage / Decimal('100')
        else:
            settings = LoyaltySettings.get_settings()
            cutoff   = timezone.now() - timedelta(days=settings.period_days)
            stats    = Order.objects.filter(
                customer_phone=self.customer_phone,
                status='completed',
                created_at__gte=cutoff,
            ).aggregate(jumlah=Count('id'), total=Sum('total_price'))

            is_loyal = (
                (stats['jumlah'] or 0) >= settings.min_orders
                and (stats['total'] or Decimal('0')) >= settings.min_spending
            )
            rate = settings.discount_percentage / Decimal('100') if is_loyal else Decimal('0')

        if rate > 0:
            self.discount_amount = (self.subtotal * rate).quantize(Decimal('1'))
            self.total_price     = self.subtotal - self.discount_amount
            self.save(update_fields=['discount_amount', 'total_price'])


# ─────────────────────────────────────────────
# ORDER ITEM
# ─────────────────────────────────────────────

class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu     = models.ForeignKey(Menu,  on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(max_digits=10, decimal_places=0)
    notes = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.menu.name} x{self.quantity}"

    @property
    def subtotal(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.menu.price
        super().save(*args, **kwargs)


# ─────────────────────────────────────────────
# LOYALTY SETTINGS  (singleton)
# ─────────────────────────────────────────────

class LoyaltySettings(models.Model):
    min_orders = models.PositiveIntegerField(
        default=10,
        help_text="Minimal jumlah pesanan dalam periode",
    )
    min_spending = models.DecimalField(
        max_digits=12, decimal_places=0, default=100000,
        help_text="Minimal total belanja dalam periode (Rp)",
    )
    period_days = models.PositiveIntegerField(
        default=30,
        help_text="Periode pengecekan (hari)",
    )
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=10,
        help_text="Diskon otomatis untuk LOYAL MEMBER (%)",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Loyalty Settings"
        verbose_name_plural = "Loyalty Settings"

    def __str__(self):
        return (
            f"Min {self.min_orders}x / "
            f"Rp{self.min_spending} / "
            f"{self.period_days} hari → {self.discount_percentage}%"
        )

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ─────────────────────────────────────────────
# CUSTOMER LOYALTY
# ─────────────────────────────────────────────

class CustomerLoyalty(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    name  = models.CharField(max_length=100, blank=True)

    special_discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="Diskon manual dari admin — override aturan umum loyalty",
    )

    points      = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=14, decimal_places=0, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering        = ['-total_spent']
        verbose_name    = "Customer Loyalty"
        verbose_name_plural = "Customer Loyalties"

    def __str__(self):
        return f"{self.name or 'Unknown'} ({self.phone})"


# ─────────────────────────────────────────────
# SIGNALS
# ─────────────────────────────────────────────

@receiver(pre_save, sender=Order)
def _track_previous_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._previous_status = Order.objects.get(pk=instance.pk).status
        except Order.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


@receiver(post_save, sender=Order)
def _update_loyalty_on_complete(sender, instance, created, **kwargs):
    previous_status = getattr(instance, '_previous_status', None)

    if (
        instance.status == 'completed'
        and previous_status != 'completed'
        and instance.customer_phone
    ):
        loyalty, _ = CustomerLoyalty.objects.get_or_create(
            phone=instance.customer_phone,
            defaults={'name': instance.customer_name},
        )

        earned_points        = int(instance.total_price // 10000)
        loyalty.points      += earned_points
        loyalty.total_spent += instance.total_price

        if instance.customer_name and not loyalty.name:
            loyalty.name = instance.customer_name

        loyalty.save()


def generate_order_number():
    date_part = datetime.now().strftime("%y%m%d")

    while True:
        random_part = "".join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=4
            )
        )

        code = f"MSM-{date_part}-{random_part}"

        if not Order.objects.filter(order_number=code).exists():
            return code

