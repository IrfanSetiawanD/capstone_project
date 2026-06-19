# menu/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from order.permissions import PublicReadStaffWrite
from .models import Menu
from .serializers import MenuSerializer

@api_view(['GET', 'POST'])
@permission_classes([PublicReadStaffWrite])
def get_menus(request):
    if request.method == 'GET':
        category_param = request.query_params.get('category')
        menus = Menu.objects.filter(is_active=True)
        
        if category_param:
            menus = menus.filter(category__name=category_param)
            
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['PUT', 'DELETE'])
@permission_classes([PublicReadStaffWrite])
def menu_detail(request, pk):
    try:
        menu = Menu.objects.get(pk=pk)
    except Menu.DoesNotExist:
        return Response({"error": "Menu tidak ditemukan"}, status=404)

    if request.method == 'PUT':
        serializer = MenuSerializer(menu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Menu berhasil diupdate"})
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        menu.delete()
        return Response({"message": "Menu berhasil dihapus"})