from django.urls import path
from .views import get_menus, menu_detail

urlpatterns = [
    path('menus/', get_menus, name='menu-list-create'),
    path('menus/<int:pk>/', menu_detail, name='menu-detail'),
]