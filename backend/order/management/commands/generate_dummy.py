import random
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone

# Sesuaikan import dengan nama aplikasi tempat model lu berada
from menu.models import Menu
from order.models import Order, OrderItem, LoyaltySettings


class Command(BaseCommand):
    help = "Generate data dummy bersih transaksi Masashimura dengan trigger pelanggan loyal."

    def handle(self, *args, **options):
        # 1. BERSIHKAN SEMUA DATA LAMA
        self.stdout.write(self.style.WARNING("Menghapus semua data order lama dari database..."))
        Order.objects.all().delete()

        # 2. Ambil semua menu yang tersedia di database
        menus = list(Menu.objects.all())
        if not menus:
            self.stdout.write(
                self.style.ERROR(
                    "Database menu kosong! Masukkan data menu terlebih dahulu."
                )
            )
            return

        # 3. Definisikan nomor telepon khusus untuk Trigger Loyalty (>10 pesanan berbeda hari)
        loyal_customers = [
            {
                "phone": "081234567890",
                "name": "Budi Setiawan",
                "orders_count": 13,
            },
            {
                "phone": "089876543210",
                "name": "Bambang Sahputra",
                "orders_count": 18,
            },
            {
                "phone": "085711223344",
                "name": "Rian Hidayat",
                "orders_count": 10,
            },
        ]

        # 4. Buat list nomor telepon acak biasa (pesanan dikit, tidak loyal)
        casual_customers = [
            {"phone": f"0813{random.randint(10000000, 99999999)}", "name": f"Pelanggan {i}"}
            for i in range(1, 25)
        ]

        now = timezone.now()
        total_orders_created = 0
        
        # Counter untuk mengunci tepat 5-6 pesanan yang belum lunas
        target_unpaid_count = random.randint(5, 6)
        unpaid_created = 0

        # --- GENERATE PELANGGAN LOYAL (Semua Lunas) ---
        self.stdout.write("Generating pelanggan loyal...")
        for cust in loyal_customers:
            for day_offset in range(cust["orders_count"]):
                order_date = now - timedelta(
                    days=(day_offset * 2) + random.randint(0, 1)
                )

                order = Order.objects.create(
                    source=random.choice(["web", "pos"]),
                    status="completed",
                    payment_status="paid",
                    payment_method=random.choice(["cash", "qris", "qris_manual"]),
                    is_deferred_payment=False,
                    customer_name=cust["name"],
                    customer_phone=cust["phone"],
                    table_number=str(random.randint(1, 15)),
                    kasir_name=random.choice(["Irfan", "Iqbal", "Sistem"]),
                )

                # Override created_at masa lalu
                Order.objects.filter(pk=order.pk).update(created_at=order_date)

                selected_menus = random.sample(
                    menus, k=random.randint(2, min(4, len(menus)))
                )
                for menu in selected_menus:
                    OrderItem.objects.create(
                        order=order,
                        menu=menu,
                        quantity=random.randint(1, 3),
                        price=menu.price,
                    )

                order.recalculate_totals()
                total_orders_created += 1

        # --- GENERATE PELANGGAN BIASA (Disisipkan 5-6 Belum Lunas) ---
        self.stdout.write("Generating pelanggan biasa...")
        for cust in casual_customers:
            for _ in range(random.randint(1, 3)):
                order_date = now - timedelta(
                    days=random.randint(0, 30),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59),
                )

                # Tentukan secara acak apakah order ini dijadikan transaksi 'Belum Lunas'
                if unpaid_created < target_unpaid_count and random.choice([True, False, False]):
                    status = "pending"
                    payment_status = "unpaid"
                    payment_method = None
                    is_deferred_payment = True  # Makan dulu, bayar nanti (POS)
                    unpaid_created += 1
                else:
                    status = "completed"
                    payment_status = "paid"
                    payment_method = random.choice(["cash", "qris", "qris_manual"])
                    is_deferred_payment = False

                order = Order.objects.create(
                    source=random.choice(["web", "pos"]) if status == "completed" else "pos",
                    status=status,
                    payment_status=payment_status,
                    payment_method=payment_method,
                    is_deferred_payment=is_deferred_payment,
                    customer_name=cust["name"],
                    customer_phone=cust["phone"],
                    table_number=str(random.randint(1, 15)),
                    kasir_name=random.choice(["Irfan", "Iqbal"]),
                )
                
                Order.objects.filter(pk=order.pk).update(created_at=order_date)

                selected_menus = random.sample(
                    menus, k=random.randint(1, min(2, len(menus)))
                )
                for menu in selected_menus:
                    OrderItem.objects.create(
                        order=order,
                        menu=menu,
                        quantity=random.randint(1, 2),
                        price=menu.price,
                    )

                order.recalculate_totals()
                total_orders_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\n[SUKSES] Database dibersihkan! Berhasil generate total {total_orders_created} order baru."
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"-> {unpaid_created} transaksi disisakan dengan status BELUM LUNAS (Unpaid)."
            )
        )