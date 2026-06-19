from django.urls import path
from .views import (
    create_order, 
    list_orders, 
    DashboardStatsView, 
    check_loyalty_status
)

urlpatterns = [
    # Endpoint untuk membuat pesanan
    path('orders/', create_order, name='create-order'),
    
    # Endpoint untuk mengambil daftar pesanan (Admin)
    path('orders/list/', list_orders, name='list_orders'),
    
    # Endpoint untuk mengecek status loyalitas pelanggan (Frontend)
    path('check-loyalty/', check_loyalty_status, name='check-loyalty'),
    
    # Endpoint untuk statistik dashboard (Admin)
    path('stats/dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
]