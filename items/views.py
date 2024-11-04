from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .filters import ProductFilter
from django.db.models import Min, Max
from drf_yasg.utils import swagger_auto_schema

from .models import Product, ProductVariant, Review, Category
from .serializers import ProductSerializer, ProductVariantSerializer, ReviewSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        """List all categories."""
        return super().list(request, *args, **kwargs)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_queryset(self):

        queryset = Product.objects.annotate(
            min_price=Min('variants__additional_price'),
            max_price=Max('variants__additional_price')
        )

        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')

        if price_min and price_min.isdigit():
            queryset = queryset.filter(min_price__gte=float(price_min))

        if price_max and price_max.isdigit():
            queryset = queryset.filter(max_price__lte=float(price_max))

        return queryset

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer

    def list(self, request, *args, **kwargs):
        """List all product variants."""
        return super().list(request, *args, **kwargs)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]  

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        variant_id = self.request.data.get('variant')
        try:
            variant = ProductVariant.objects.get(id=variant_id)
        except ProductVariant.DoesNotExist:
            return Response({"error": "Variant not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer.save(user=self.request.user, variant=variant)
