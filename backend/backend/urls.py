from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('menu.urls')),   # Mengakses api/menus/ & api/menus/<id>/
    path('api/', include('order.urls')),  # Mengakses api/orders/ & api/stats/dashboard/
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)