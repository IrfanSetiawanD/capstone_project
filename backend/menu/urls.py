from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, TopBestSellersMenuView

router = DefaultRouter()
router.register(r'menus', MenuViewSet, basename='menu')

urlpatterns = [
    # Path manual untuk bestsellers HARUS di atas agar tidak "dimakan" router
    path('menus/bestsellers/', TopBestSellersMenuView.as_view(), name='menu-bestsellers'),

    # Semua path CRUD menu lainnya (GET, POST, PUT, DELETE)
    path('', include(router.urls)),
]