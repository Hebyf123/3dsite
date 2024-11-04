from django.test import TestCase
from cart.models import Cart, CartItem, Order, OrderItem
from django.contrib.auth import get_user_model
from items.models import Product, ProductVariant, Category

User = get_user_model()

class CartModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')  
        self.user = User.objects.create_user(email='test@example.com', password='password')
        self.product = Product.objects.create(name='Test Product', description='A test product', category=self.category)  
        self.variant = ProductVariant.objects.create(product=self.product, color='Red', additional_price=1.00, stock=5)
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_total_cost(self):
        CartItem.objects.create(cart=self.cart, variant=self.variant, quantity=3)
        self.cart.refresh_from_db()  # Обновляем данные корзины
        expected_total_cost = 3 * (self.variant.price + self.variant.additional_price)  
        self.assertEqual(self.cart.total_cost(), expected_total_cost)


    def test_add_product_to_cart(self):
        self.cart.add_product(self.variant, quantity=2)
        self.cart.refresh_from_db()  
        self.assertEqual(self.cart.items.count(), 1)  
        self.assertEqual(self.cart.items.first().quantity, 2)  

    def test_remove_product_from_cart(self):
        self.cart.add_product(self.variant, quantity=2)
        self.cart.remove_product(self.variant)
        self.cart.refresh_from_db()  
        self.assertEqual(self.cart.items.count(), 0)  

    def test_create_order(self):
        self.cart.add_product(self.variant, quantity=2)
        order = self.cart.create_order('123 Street', 'City', 'Country', '123456789')
        self.assertEqual(order.total_cost, self.cart.total_cost())  
        self.assertEqual(order.order_items.count(), 1)  
