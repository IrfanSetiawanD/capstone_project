from rest_framework import serializers
from .models import Menu, Category


class MenuSerializer(serializers.ModelSerializer):
    category      = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_name = serializers.CharField(source="category.name", read_only=True)
    image         = serializers.ImageField(write_only=True, required=False, allow_null=True)
    image_url     = serializers.SerializerMethodField(read_only=True)
    price_web     = serializers.DecimalField(max_digits=10, decimal_places=0, read_only=True)

    class Meta:
        model  = Menu
        fields = [
            "id", "name", "price", "price_web",
            "category", "category_name",
            "description", "image", "image_url",
            "is_available", "is_active",
        ]

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None