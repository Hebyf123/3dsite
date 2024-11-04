from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CartViewSet,OrderViewSet,DiscountViewSet,create_checkout_session,stripe_webhook
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi
router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'discounts', DiscountViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API для работы с продуктами, категориями, вариантами и отзывами.",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,  
    permission_classes=(permissions.IsAdminUser,),
)

urlpatterns = [
    path('', include(router.urls)),
    path('create-checkout-session/',create_checkout_session,name='create-session'),
    path('webhook/stripe/', stripe_webhook, name='stripe-webhook'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]