from rest_framework import serializers
from .models import Menu

class MenuSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'name', 'category', 'price', 'stock', 'is_active', 'image_url']

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None