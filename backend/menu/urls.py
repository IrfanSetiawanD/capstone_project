# menu/urls.py
from django.urls import path
from core.views import get_menus   # atau dari menu.views kalau sudah dipindah

urlpatterns = [
    path('', get_menus, name='get-menus'),
]