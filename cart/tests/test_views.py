from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cart.models import Cart, Order
from items.models import ProductVariant, Product, Category 
from django.contrib.auth import get_user_model

User = get_user_model()

class CartViewSetTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')  # Создание категории
        self.user = User.objects.create_user(email='test@example.com', password='password')
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name='Test Product', description='A test product', category=self.category)  
        self.variant = ProductVariant.objects.create(product=self.product, color='Red', additional_price=1.00, stock=5)  
        self.cart = Cart.objects.create(user=self.user)

    def test_list_cart(self):
        response = self.client.get(reverse('cart-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_product_to_cart(self):
        response = self.client.post(reverse('cart-add-product'), data={'variant_id': self.variant.id, 'quantity': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart.refresh_from_db()  
        self.assertEqual(self.cart.items.count(), 1)

    def test_remove_product_from_cart(self):
        self.cart.add_product(self.variant, quantity=2)
        response = self.client.post(reverse('cart-remove-product'), data={'variant_id': self.variant.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart.refresh_from_db()  
        self.assertEqual(self.cart.items.count(), 0)

    def test_create_order(self):
        self.cart.add_product(self.variant, quantity=2)
        response = self.client.post(reverse('order-list'), data={
            'address': '123 Street',
            'city': 'City',
            'country': 'Country',
            'phone': '123456789',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
