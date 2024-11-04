from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import URLPattern, path
from django.views.generic import RedirectView
from .views import google_login, auth_callback
from . import views
router = DefaultRouter()
#router.register(r'users', views.UserViewSet, basename='user')
#router.register(r'oauth-login/', views.OAuthLoginViewSet, basename='oauth-login')
#router.register(r'telegram', views.TelegramTokenViewSet, basename='telegram')
urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', google_login, name='google_login'),
    path('auth/callback/', auth_callback, name='auth_callback'),
]

