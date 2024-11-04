from django.contrib import admin
from .models import Category, Product, ProductVariant,Review


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    fields = ('color', 'additional_price', 'stock', 'model_file', 'thumbnail', 'image')
    readonly_fields = ('price',) 
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('product', 'rating')
    search_fields = ('text',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')  
    search_fields = ('name',)  
    readonly_fields = ('created', 'modified')  


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'availability_status', 'created', 'modified')  
    list_filter = ('category', 'created', 'modified')  
    search_fields = ('name', 'category__name')  
    inlines = [ProductVariantInline]  
    readonly_fields = ('created', 'modified', 'price', 'is_available', 'availability_status')  

    def price(self, obj):
        return obj.price

    def is_available(self, obj):
        return obj.is_available

    def availability_status(self, obj):
        return obj.availability_status

    price.short_description = 'Цена'
    is_available.short_description = 'Доступен?'
    availability_status.short_description = 'Статус наличия'


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'additional_price', 'stock', 'price')  
    list_filter = ('product', 'color')  
    search_fields = ('product__name', 'color')  
    readonly_fields = ('price',)  

    def price(self, obj):
        return obj.price

    price.short_description = 'Цена варианта'
