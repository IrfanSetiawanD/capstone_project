# accounts/urls.py
from django.urls import path
from .views import CustomAuthToken, create_user_view

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='api-login'),
    path('users/create/', create_user_view, name='api-create-user'), # URL pas dengan userAPI.createUser di FE
]