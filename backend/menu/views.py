from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Menu
from .serializers import MenuSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.filter(is_active=True)
    serializer_class = MenuSerializer
    permission_classes = [AllowAny]   # ← Tambahkan ini

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset