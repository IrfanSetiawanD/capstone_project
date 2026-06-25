from rest_framework import serializers
from .models import Menu, Category


class MenuSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    # Field untuk upload gambar (write only)
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    # Field untuk menampilkan URL gambar (read only)
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Menu
        fields = [
            "id",
            "name",
            "price",
            "category",
            "description",
            "image",
            "image_url",
            "is_available",
            "is_active",
        ]

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None
