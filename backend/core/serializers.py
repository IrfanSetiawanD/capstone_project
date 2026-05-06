from rest_framework import serializers

class OrderItemInputSerializer(serializers.Serializer):
    menu_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


class OrderSerializer(serializers.Serializer):
    phone = serializers.CharField()
    items = OrderItemInputSerializer(many=True)
    payment_method = serializers.CharField()