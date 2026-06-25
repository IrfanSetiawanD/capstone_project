from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Sum
import cloudinary.uploader

from .models import Menu
from .serializers import MenuSerializer
from order.permissions import PublicReadStaffWrite


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [PublicReadStaffWrite]

    def perform_update(self, serializer):
        """
        Kalau ada gambar baru dikirim saat update, hapus gambar lama
        di Cloudinary dulu sebelum data baru disimpan.
        """
        instance = self.get_object()
        new_image = self.request.FILES.get('image')

        if new_image and instance.image:
            try:
                cloudinary.uploader.destroy(instance.image.public_id)
            except Exception as e:
                print(f"[Cloudinary] Gagal hapus gambar lama Menu id={instance.pk}: {e}")

        serializer.save()

    # perform_destroy TIDAK perlu di-override.
    # Penghapusan gambar Cloudinary saat delete sudah otomatis
    # ditangani oleh signal post_delete di models.py — jadi tidak dobel.


class TopBestSellersMenuView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # 1. Annotate & filter menu berdasarkan jumlah terjual
        top_menus = Menu.objects.annotate(
            total_ordered=Sum('orderitem__quantity')
        ).filter(total_ordered__gt=0).order_by('-total_ordered')[:3]

        # 2. Fallback jika belum ada yang terjual
        if not top_menus.exists():
            top_menus = Menu.objects.filter(is_active=True)[:3]

        # 3. Pakai serializer yang sama supaya format response konsisten
        serializer = MenuSerializer(top_menus, many=True)
        return Response(serializer.data)
