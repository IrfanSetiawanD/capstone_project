from django.urls import path
from .views import (
    list_orders,
    get_order,
    create_order,
    check_loyalty_status,
    loyal_customers,
    order_reports,
    active_orders_per_day,
    DashboardStatsView,
    LoyaltySettingsView,
    LoyalCustomersView,
    GiveSpecialPriceView,
    admin_dashboard_daily_stats,
    export_excel_report,
    export_pdf_report,
    unpaid_orders,
    pay_order,
    order_history,
    finance_monthly_summary,
    finance_daily_summary,
)

app_name = "orders"

urlpatterns = [
    # ── Orders CRUD ──────────────────────────────────────────────────────────
    path("orders/",          create_order, name="order-create"),
    path("orders/list/",     list_orders,  name="order-list"),

    # PENTING: semua path statis HARUS di atas <int:pk>
    # agar Django tidak mencoba cast string ke integer dan gagal 404.

    # ── Loyalty — publik ─────────────────────────────────────────────────────
    path("orders/check_loyalty_status/", check_loyalty_status, name="check-loyalty"),
    path("orders/loyal/",                loyal_customers,       name="loyal-customers"),

    # ── Loyalty — admin ──────────────────────────────────────────────────────
    path("orders/loyalty-settings/",               LoyaltySettingsView.as_view(),  name="loyalty-settings"),
    path("orders/loyal-customers/",                LoyalCustomersView.as_view(),   name="loyal-customers-admin"),
    path("orders/give-special-price/<str:phone>/", GiveSpecialPriceView.as_view(), name="give-special-price"),

    # ── Reports & dashboard ──────────────────────────────────────────────────
    path("orders/reports/",                        order_reports,                name="order-reports"),
    path("orders/stats/",                          DashboardStatsView.as_view(), name="dashboard-stats"),
    path("orders/admin_dashboard_daily_stats/",    admin_dashboard_daily_stats,  name="admin-daily-stats"),
    path("orders/export_excel_report/",            export_excel_report,          name="export-excel"),
    path("orders/export_pdf_report/",              export_pdf_report,            name="export-pdf"),
    path("orders/finance/monthly/", finance_monthly_summary, name="finance-monthly"),
    path("orders/finance/daily/",   finance_daily_summary,   name="finance-daily"),

    # ── Tagihan belum lunas & riwayat ─────────────────────────────────────────
    path("orders/unpaid/",   unpaid_orders, name="unpaid-orders"),
    path("orders/history/",  order_history, name="order-history"),

    # ── Active orders (prefix berbeda) ────────────────────────────────────────
    path("active-orders/",   active_orders_per_day, name="active-orders"),

    # ── Detail & pay — HARUS PALING BAWAH karena pakai <int:pk> ─────────────
    path("orders/<int:pk>/",      get_order, name="order-detail"),
    path("orders/<int:pk>/pay/",  pay_order, name="pay-order"),
]
