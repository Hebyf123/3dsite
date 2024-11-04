from rest_framework import serializers
from .models import Cart, CartItem,Order,OrderItem,Discount
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['variant', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_cost', 'address', 'city', 'country', 'phone', 'payment_status', 'stripe_payment_intent_id', 'created_at']

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='variant.product.name', read_only=True)
    product_color = serializers.CharField(source='variant.color', read_only=True)
    product_price = serializers.DecimalField(source='variant.price', max_digits=10, decimal_places=2, read_only=True)
    variant_id = serializers.IntegerField(source='variant.id', read_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'product_name', 'product_color', 'product_price', 'variant_id','quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_cost']
class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'code', 'percentage', 'start_date', 'end_date', 'is_active']