from rest_framework import serializers
from .models import ProductVariant, Product,Review,Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'color', 'additional_price', 'stock', 'price', 'model_file', 'thumbnail', 'image']

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    price = serializers.DecimalField(source='min_price', max_digits=10, decimal_places=2, read_only=True)
    price_max = serializers.DecimalField(source='max_price', max_digits=10, decimal_places=2, read_only=True)
    image = serializers.CharField( read_only=True)
    model_file = serializers.CharField(  read_only=True)
   
    class Meta:
        model = Product
        fields = ['id', 'name', 'description','image', 'model_file',  'price','price_max', 'category', 'availability_status', 'variants']
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'user','variant', 'rating', 'text', 'created_at', 'parent']