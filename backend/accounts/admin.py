from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

# Inline UserProfile di halaman User
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Register ulang User dengan inline
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register UserProfile juga
admin.site.register(UserProfile)