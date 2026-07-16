# nama file: generate_dummy.py (atau di dalam folder management/commands)
import random
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Sum

from menu.models import Menu
from order.models import Order, OrderItem, LoyaltySettings, CustomerLoyalty

class Command(BaseCommand):
    help = "Generate data dummy bersih transaksi lunas Masashimura dan rebuild saldo poin loyalty."

    def handle(self, *args, **options):
        # 1. BERSIHKAN SEMUA DATA LAMA
        self.stdout.write(self.style.WARNING("Menghapus semua data order dan loyalty lama dari database..."))
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        CustomerLoyalty.objects.all().delete()

        # 2. Ambil semua menu yang tersedia
        menus = list(Menu.objects.all())
        if not menus:
            self.stdout.write(
                self.style.ERROR(
                    "Database menu kosong! Masukkan data menu terlebih dahulu."
                )
            )
            return

        # Pastikan pengaturan poin ada (Rupiah per Poin)
        settings = LoyaltySettings.get_settings()
        rate_poin = settings.rupiah_per_point or 10000

        # 3. Definisikan nomor telepon "loyal" (pesanan banyak, poin melimpah)
        loyal_customers = [
            {"phone": "081234567890", "name": "Budi Setiawan",    "orders_count": 33},
            {"phone": "089876543210", "name": "Bambang Sahputra", "orders_count": 58},
            {"phone": "085711223344", "name": "Rian Hidayat",     "orders_count": 43},
            {"phone": "085761879278", "name": "Dadang Kusnandar",     "orders_count": 20},
            {"phone": "088900223421", "name": "Ismail Komar",     "orders_count": 5},
        ]

        # 4. Buat list pelanggan acak biasa (pesanan sedikit)
        casual_customers = [
            {"phone": f"0813{random.randint(10000000, 99999999)}", "name": f"Pelanggan {i}"}
            for i in range(1, 25)
        ]

        now = timezone.now()
        total_orders_created = 0

        # --- FUNGSI HELPER UNTUK BUAT ORDER LUNAS ---
        def create_paid_order(cust, order_date):
            order = Order.objects.create(
                source=random.choice(["web", "pos"]),
                status="completed",
                payment_status="paid",
                payment_method=random.choice(["cash", "qris", "qris_manual"]),
                is_deferred_payment=False,
                customer_name=cust["name"],
                customer_phone=cust["phone"],
                table_number=str(random.randint(1, 15)),
                kasir_name=random.choice(["Irfan Setiawan Dawolo", "Muhammad Iqbal", "Sistem"]),
            )
            
            # Override created_at ke masa lalu
            Order.objects.filter(pk=order.pk).update(created_at=order_date)

            selected_menus = random.sample(menus, k=random.randint(2, min(4, len(menus))))
            for menu in selected_menus:
                OrderItem.objects.create(
                    order=order,
                    menu=menu,
                    quantity=random.randint(1, 3),
                    price=menu.price,
                )
            order.recalculate_totals()
            return order

        # --- GENERATE PELANGGAN LOYAL ---
        self.stdout.write("Generating pesanan pelanggan loyal (Sistem Poin)...")
        for cust in loyal_customers:
            for day_offset in range(cust["orders_count"]):
                # Order tersebar di masa lalu
                order_date = now - timedelta(days=(day_offset * 2) + random.randint(0, 1))
                create_paid_order(cust, order_date)
                total_orders_created += 1

        # --- GENERATE PELANGGAN BIASA ---
        self.stdout.write("Generating pesanan pelanggan kasual (Sistem Poin)...")
        for cust in casual_customers:
            for _ in range(random.randint(1, 3)):
                order_date = now - timedelta(
                    days=random.randint(0, 30),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59),
                )
                create_paid_order(cust, order_date)
                total_orders_created += 1

        # --- REBUILD SALDO POIN PELANGGAN ---
        self.stdout.write(self.style.WARNING("Merekonstruksi ulang saldo poin dan histori belanja..."))
        
        # Kosongkan data CustomerLoyalty
        CustomerLoyalty.objects.all().delete()
        
        # PERBAIKAN: Gunakan .order_by() kosong untuk mematikan default ordering
        # lalu bungkus dengan set() agar dijamin 100% unik
        phone_numbers = set(
            Order.objects.exclude(customer_phone="")
            .order_by()
            .values_list("customer_phone", flat=True)
        )
        
        for phone in phone_numbers:
            cust_orders = Order.objects.filter(customer_phone=phone, payment_status="paid").order_by("created_at")
            if not cust_orders.exists():
                continue
                
            first_order = cust_orders.first()
            last_order = cust_orders.last()
            
            # Hitung total belanja
            total_spent_aggr = cust_orders.aggregate(total=Sum("total_price"))["total"] or Decimal("0")
            total_spent = int(total_spent_aggr)
            
            # Hitung poin berdasarkan rate (asumsi belum ada poin yang di-redeem/ditukar)
            calculated_points = total_spent // rate_poin
            
            # PERBAIKAN: Gunakan update_or_create untuk mencegah bentrok unique constraint
            CustomerLoyalty.objects.update_or_create(
                phone=phone,
                defaults={
                    "name": first_order.customer_name,
                    "points": calculated_points,
                    "total_orders": cust_orders.count(),
                    "total_spent": total_spent,
                    "last_order_at": last_order.created_at
                }
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n[SUKSES] Database dibersihkan! Berhasil generate total {total_orders_created} order KOMPLET/LUNAS."
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"-> Sistem Poin telah di-rebuild ulang sesuai rate (Rp {rate_poin} = 1 Poin)."
            )
        )