# project/urls.py (главное приложение)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/items/', include('items.urls')),  
    path('api/cart/', include('cart.urls')),    
    path('api/usersmodel',include('usersmodel.urls')),
    path('rosetta/', include('rosetta.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)