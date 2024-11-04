from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from items.models import Product, ProductVariant, Category

class ProductViewSetTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Fruits')
        self.product = Product.objects.create(name='Apple', description='Fresh apple', category=self.category)
        self.variant = ProductVariant.objects.create(product=self.product, color='Red', additional_price=1.00, stock=5)

    def test_list_products(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        response = self.client.post(reverse('product-list'), data={
            'name': 'Banana',
            'description': 'Yellow banana',
            'category': self.category.id,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_product_variant_view(self):
        response = self.client.get(reverse('productvariant-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
