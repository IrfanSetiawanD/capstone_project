from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Sum, Q
from django.db.models.deletion import ProtectedError
from rest_framework import viewsets, status

from .models import Menu, Category
from .serializers import MenuSerializer, CategorySerializer
from order.permissions import PublicReadStaffWrite


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [PublicReadStaffWrite]


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.select_related("category").all()
    serializer_class = MenuSerializer
    permission_classes = [PublicReadStaffWrite]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError:
            instance.is_active = False
            instance.is_available = False
            instance.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            return Response(
                {"detail": "Menu berhasil dihapus."},
                status=status.HTTP_204_NO_CONTENT
            )
        except ProtectedError:
            instance.is_active = False
            instance.is_available = False
            instance.save()
            return Response(
                {"detail": "Menu memiliki riwayat order, dinonaktifkan.", "deactivated": True},
                status=status.HTTP_200_OK
            )


class TopBestSellersMenuView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        top_menus = (
            Menu.objects.annotate(
                total_ordered=Sum(
                    'orderitem__quantity',
                    filter=Q(orderitem__order__status='completed'),
                )
            )
            .filter(total_ordered__gt=0, is_active=True)
            .order_by('-total_ordered')[:3]
        )

        if not top_menus.exists():
            top_menus = Menu.objects.filter(is_active=True, is_available=True)[:3]

        serializer = MenuSerializer(top_menus, many=True)
        return Response(serializer.data)