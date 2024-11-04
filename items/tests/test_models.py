from django.test import TestCase
from items.models import Product, ProductVariant, Category
from decimal import Decimal

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Fruits')
        self.product = Product.objects.create(name='Apple', description='Fresh apple', category=self.category)
        self.variant = ProductVariant.objects.create(product=self.product, color='Red', additional_price=Decimal('1.00'), stock=5)

    def test_product_price(self):
        # Проверяем, что цена продукта равна цене его варианта
        expected_price = self.variant.additional_price  # Учитываем, что у продукта нет базовой цены
        self.assertEqual(self.product.price, expected_price)

    def test_product_availability(self):
        self.assertTrue(self.product.is_available)

    def test_variant_price(self):
        # Ожидаемая цена варианта равна его дополнительной цене
        expected_price = self.variant.additional_price
        self.assertEqual(self.variant.price, expected_price)

    def test_variant_str(self):
        self.assertEqual(str(self.variant), f"{self.product.name} - {self.variant.color}")
