from django.db import models
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel
from easy_thumbnails.fields import ThumbnailerImageField
from django.conf import settings

class Category(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name=_('Название категории'))

    def __str__(self):
        return self.name

class Product(TimeStampedModel):
	name = models.CharField(max_length=255, verbose_name=_('Название продукта'))
	description = models.TextField(verbose_name=_('Описание'))
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name=_('Категория'))

	@property
	def price(self):
		if self.variants.exists():
			cheapest_variant = min(self.variants.all(), key=lambda v: v.price)
			return cheapest_variant.price
		return 0  
	
	@property
	def price_max(self):
		if self.variants.exists():
			most_expensive_variant = max(self.variants.all(), key=lambda v: v.price)
			return most_expensive_variant.price
		return 0 
	
	@property
	def image(self):
		if self.variants.exists():
			cheapest_variant = min(self.variants.all(), key=lambda v: v.price)
			return "http://localhost:8001"+cheapest_variant.image.url if cheapest_variant.image else None
		return None

	@property
	def model_file(self):
		if self.variants.exists():
			cheapest_variant = min(self.variants.all(), key=lambda v: v.price)
			return "http://localhost:8001"+cheapest_variant.model_file.url if cheapest_variant.model_file else None
		return None

	@property
	def is_available(self):
		return any(variant.stock > 0 for variant in self.variants.all())	
	
	@property
	def availability_status(self):
		return _('Доступен') if self.is_available else _('Недоступен')	
	
	@property
	def average_rating(self):
		reviews = self.reviews.all()
		if reviews.exists():
		    return sum(review.rating for review in reviews) / reviews.count()
		return 0	
	
	@property
	def review_count(self):
		return self.reviews.count()	
	def __str__(self):
		return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name=_('Продукт'))
    color = models.CharField(max_length=100, verbose_name=_('Цвет'))
    additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_('Дополнительная цена'))
    stock = models.PositiveIntegerField(verbose_name=_('Количество на складе'))
    model_file = models.FileField(upload_to='3d_models/', verbose_name=_('3D модель'), blank=True, null=True)
    thumbnail = ThumbnailerImageField(upload_to='product_thumbnails/', blank=True, null=True, verbose_name=_('Миниатюра'))
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name=_('Изображение'))

    @property
    def price(self):
        return self.additional_price  
    def __str__(self):
        return f"{self.product.name} - {self.color}"
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('Продукт'))
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Пользователь'))  
    rating = models.PositiveIntegerField(default=1, verbose_name=_('Оценка'), choices=[(i, str(i)) for i in range(1, 6)])  
    text = models.TextField(verbose_name=_('Отзыв'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies', verbose_name=_('Родительский отзыв')) 
    def __str__(self):
        return f'Отзыв от {self.user} на {self.product}'

    class Meta:
        ordering = ['-created_at']  