from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from items.models import Product, ProductVariant
from decimal import Decimal
import stripe
from django.core.exceptions import ValidationError
from django.utils import timezone
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user}"

    def total_cost(self):
        return sum(item.total_price() for item in self.items.all())

    def add_product(self, variant, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(cart=self, variant=variant)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity  
        cart_item.save()

    def remove_product(self, variant):
        CartItem.objects.filter(cart=self, variant=variant).delete()

    def update_quantity(self, variant, quantity):
        cart_item = CartItem.objects.get(cart=self, variant=variant)
        cart_item.quantity = quantity
        cart_item.save()

    def create_order(self, address, city, country, phone):
        order = Order.objects.create(
            user=self.user,
            cart=self,
            address=address,
            city=city,
            country=country,
            phone=phone
        )
        
        for item in self.items.all():
            OrderItem.objects.create(order=order, variant=item.variant, quantity=item.quantity)
        
        return order


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.variant.product.name} (Color: {self.variant.color})"

    def total_price(self):
        additional_price = Decimal(self.variant.additional_price)
        product_price = Decimal(self.variant.product.price)  
        return self.quantity * (product_price + additional_price)


stripe.api_key = 'sk_test_51Q6UI8Ca7V035Tb0Cn8M0ctf2lzUCTKWu6x09uy2npyT1J8OvhI9P6ZOAtJPsfjgI60YVSYfdTNFpXlbgh0eqbJq00NbdadbCd'
class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_('Код купона'))
    percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Процент скидки'))
    start_date = models.DateTimeField(verbose_name=_('Дата начала'))
    end_date = models.DateTimeField(verbose_name=_('Дата окончания'))
    is_active = models.BooleanField(default=True, verbose_name=_('Активен'))

    def is_valid(self):
        return self.is_active and self.start_date <= timezone.now() <= self.end_date

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('Скидка')
        verbose_name_plural = _('Скидки')
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discounted_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    address = models.CharField(max_length=255, verbose_name="Адрес")
    city = models.CharField(max_length=255, verbose_name="Город")
    country = models.CharField(max_length=255, verbose_name="Страна")
    phone = models.CharField(max_length=255, verbose_name="Телефон")
    payment_status = models.CharField(max_length=20, default='pending')  # 'pending', 'paid', 'failed'
    stripe_payment_intent_id = models.CharField(max_length=255, null=True, blank=True)
    coupon_code = models.CharField(max_length=50, null=True, blank=True, verbose_name="Код купона")

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"

    def save(self, *args, **kwargs):
        self.total_cost = self.cart.total_cost()   
        self.discounted_cost = self.apply_discount()  
        super().save(*args, **kwargs)

    def apply_discount(self):
        if self.coupon_code:
            try:
                discount = Discount.objects.get(code=self.coupon_code, is_active=True)
                discount_amount = self.total_cost * (discount.percentage / 100)
                return self.total_cost - discount_amount
            except Discount.DoesNotExist:
               
                return self.total_cost
        return self.total_cost  

    def create_payment_intent(self):
        intent = stripe.PaymentIntent.create(
            amount=int(self.discounted_cost * 100),  
            currency='usd',
            metadata={'order_id': self.id}
        )
        self.stripe_payment_intent_id = intent['id']
        self.save()
        return intent



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.variant.product.name} (Color: {self.variant.color})"
