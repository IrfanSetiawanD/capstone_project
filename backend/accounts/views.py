from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserCreateSerializer
from .permissions import IsOwner

class CustomAuthToken(ObtainAuthToken):
    # Mengizinkan akses publik ke endpoint login
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username') or request.data.get('email')
        password = request.data.get('password')

        # Coba autentikasi dengan username biasa
        user = authenticate(username=username, password=password)
        
        # Jika gagal, coba cari berdasarkan email
        if not user and '@' in username:
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if not user:
            return Response({"non_field_errors": ["Username/Email atau password salah"]}, status=400)

        token, _ = Token.objects.get_or_create(user=user)
        
        # Logika RBAC
        if user.is_superuser: 
            role = 'owner'
        elif user.is_staff: 
            role = 'admin'
        elif hasattr(user, 'profile'): 
            role = user.profile.role
        else: 
            role = 'pelanggan'

        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'name': user.get_full_name() or user.username,
                'role': role
            }
        })

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsOwner])
def create_user_view(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": f"User {user.username} berhasil dibuat!"}, status=201)
    return Response(serializer.errors, status=400)