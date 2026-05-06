# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user, role=role)
        return user