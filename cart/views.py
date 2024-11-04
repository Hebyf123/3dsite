from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import stripe

from .models import Cart, ProductVariant, Order, Discount
from .serializers import CartSerializer, OrderSerializer, DiscountSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
@api_view(['POST'])
def create_checkout_session(request):
    if request.method == 'POST':
        domain_url = 'http://localhost:8080/'
        line_items = build_line_items(request.data.get('items', []))

        order_id = request.data.get('order_id')
        order = get_order_by_id(order_id)

        if order is None:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='payment',
                success_url=f"{domain_url}success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{domain_url}cancelled/",
                line_items=line_items,
            )

            order.stripe_payment_intent_id = checkout_session.id
            order.save()
            return Response({'id': checkout_session.id})

        except Exception as e:
            return Response({'error': str(e)}, status=400)

def build_line_items(items):
    return [{
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': item.get('product_name', 'No Name'),
                'description': item.get('description', ''),
            },
            'unit_amount': int(float(item.get('product_price', 0)) * 100),
        },
        'quantity': item.get('quantity', 1),
    } for item in items]

def get_order_by_id(order_id):
    return Order.objects.filter(id=order_id).first()

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=OrderSerializer)
    def create(self, request, *args, **kwargs):
        cart = self.get_user_cart(request.user)
        if not cart:
            return Response({"detail": "Корзина пуста."}, status=status.HTTP_400_BAD_REQUEST)

        order = self.create_order_from_cart(cart, request.data)
        if isinstance(order, Response):
            return order

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_user_cart(self, user):
        return user.cart.first()

    def create_order_from_cart(self, cart, data):
        order = cart.create_order(
            address=data.get('address'),
            city=data.get('city'),
            country=data.get('country'),
            phone=data.get('phone')
        )
        coupon_code = data.get('coupon_code')
        if coupon_code:
            return self.apply_discount(order, coupon_code)

        order.create_payment_intent()
        return order

    def apply_discount(self, order, coupon_code):
        try:
            discount = Discount.objects.get(code=coupon_code)
            if discount.is_valid():
                discount_amount = order.total_cost * (discount.percentage / 100)
                order.total_cost -= discount_amount
                order.save()  
            else:
                return Response({"detail": "Купон недействителен."}, status=status.HTTP_400_BAD_REQUEST)
        except Discount.DoesNotExist:
            return Response({"detail": "Купон не найден."}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user).select_related('order_items__variant__product')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        order = self.get_object()
        items = order.order_items.all()
        item_list = [{
            'product': item.variant.product.name,
            'quantity': item.quantity,
            'price': item.variant.price,
            'color': item.variant.color,
        } for item in items]
        return Response({
            'order_id': order.id,
            'total_cost': order.total_cost,
            'items': item_list
        })

class CartViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: 'Cart retrieved successfully'})
    def list(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(request_body=CartSerializer)
    def add_product(self, request):
        return self.modify_cart(request, action='add')

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(request_body=CartSerializer)
    def update_product(self, request):
        return self.modify_cart(request, action='update')

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(request_body=CartSerializer)
    def remove_product(self, request):
        return self.modify_cart(request, action='remove')

    def modify_cart(self, request, action):
        variant_id = request.data.get('variant_id')
        quantity = request.data.get('quantity', 1)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        variant = ProductVariant.objects.filter(id=variant_id).first()
        if not variant:
            return Response({"error": "Variant not found."}, status=status.HTTP_404_NOT_FOUND)

        if action == 'add':
            cart.add_product(variant, quantity)
            return Response({"status": "Product added to cart"})
        elif action == 'update':
            cart.update_quantity(variant, quantity)
            return Response({"status": "Product quantity updated"})
        elif action == 'remove':
            cart.remove_product(variant)
            return Response({"status": "Product removed from cart"})

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(request_body=DiscountSerializer)
    def perform_create(self, serializer):
        serializer.save()

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    handle_webhook_event(event)
    return JsonResponse({'status': 'success'}, status=200)

def handle_webhook_event(event):
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order = get_order_by_stripe_id(session['id'])

        if order:
            order.payment_status = 'paid'
            order.save()
        else:
            return JsonResponse({'error': 'Order not found'}, status=404)


def get_order_by_stripe_id(stripe_id):
    try:
        return Order.objects.filter(stripe_payment_intent_id=stripe_id).first()
    except Order.DoesNotExist:
        return None
