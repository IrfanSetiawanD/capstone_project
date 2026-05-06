# core/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import Menu, Category


# ========================
# MENU (GET + POST)
# ========================
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def get_menus(request):
    if request.method == 'GET':
        menus = Menu.objects.filter(is_active=True)
        data = []
        for menu in menus:
            data.append({
                "id": menu.id,
                "name": menu.name,
                "category": menu.category.name,
                "price": float(menu.price),
                "stock": menu.stock,
                "is_active": menu.is_active,
                "image_url": menu.image.url if menu.image else None
            })
        return Response(data)

    # POST = Tambah Menu Baru
    name = request.data.get('name')
    category_name = request.data.get('category')
    price = request.data.get('price')
    stock = request.data.get('stock', 0)
    image = request.FILES.get('image')

    if not name or not category_name or not price:
        return Response({"error": "Nama, kategori, dan harga wajib diisi"}, status=400)

    category, _ = Category.objects.get_or_create(name=category_name)

    menu = Menu.objects.create(
        name=name,
        category=category,
        price=price,
        stock=stock,
        is_active=True
    )

    if image:
        menu.image = image
        menu.save()

    return Response({
        "id": menu.id,
        "name": menu.name,
        "category": category.name,
        "message": "Menu berhasil ditambahkan"
    }, status=201)


# ========================
# UPDATE & DELETE (untuk nanti)
# ========================
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_menu(request, pk):
    try:
        menu = Menu.objects.get(pk=pk)
    except Menu.DoesNotExist:
        return Response({"error": "Menu tidak ditemukan"}, status=404)

    menu.name = request.data.get('name', menu.name)
    menu.price = request.data.get('price', menu.price)
    menu.stock = request.data.get('stock', menu.stock)
    menu.save()
    return Response({"message": "Menu berhasil diupdate"})


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_menu(request, pk):
    try:
        menu = Menu.objects.get(pk=pk)
        menu.delete()
        return Response({"message": "Menu berhasil dihapus"})
    except Menu.DoesNotExist:
        return Response({"error": "Menu tidak ditemukan"}, status=404)


# ========================
# DASHBOARD STATS
# ========================
class DashboardStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "total_revenue": 12450000,
            "total_orders": 87,
            "top_menus": [{"name": "Beef Yakiniku"}],
            "loyal_users": [1, 2, 3]
        })