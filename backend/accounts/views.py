# accounts/views.py
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User   # ← Import ini yang kurang
from django.contrib.auth import authenticate


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Support login dengan username ATAU email
        username_or_email = request.data.get('username') or request.data.get('email')
        password = request.data.get('password')

        if not username_or_email or not password:
            return Response({"non_field_errors": ["Username/Email dan password wajib diisi"]}, status=400)

        # Coba authenticate dengan username dulu
        user = authenticate(username=username_or_email, password=password)

        # Kalau gagal, coba pakai email
        if not user:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if not user:
            return Response({"non_field_errors": ["Username/Email atau password salah"]}, status=400)

        token, _ = Token.objects.get_or_create(user=user)
        role = user.profile.role if hasattr(user, 'profile') else 'admin'

        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'name': user.get_full_name() or user.username,
                'role': role
            }
        })