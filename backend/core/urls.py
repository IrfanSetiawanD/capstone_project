# core/urls.py
from django.urls import path
from .views import get_menus, update_menu, delete_menu, DashboardStatsView

urlpatterns = [
    # GET + POST menu di endpoint yang sama
    path('menus/', get_menus, name='get_menus'),

    # Edit & Hapus menu
    path('menus/<int:pk>/', update_menu, name='update_menu'),
    path('menus/<int:pk>/', delete_menu, name='delete_menu'),

    # Stats dashboard
    path('stats/dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
]