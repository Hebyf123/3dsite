from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_cost')  
    inlines = [CartItemInline]   
    search_fields = ('user__email',)  
    readonly_fields = ('created_at', 'total_cost')  

    def total_cost(self, obj):
        return obj.total_cost()

    total_cost.short_description = 'Общая стоимость'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_cost', 'payment_status')  
    inlines = [OrderItemInline]  
    search_fields = ('user__email', 'address', 'city')  
    list_filter = ('payment_status', 'created_at')  
    readonly_fields = ('created_at', 'total_cost', 'stripe_payment_intent_id')  

    def total_cost(self, obj):
        return obj.total_cost

    total_cost.short_description = 'Общая стоимость'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'variant', 'quantity')  
    search_fields = ('order__id', 'variant__product__name')  
    list_filter = ('order__created_at',)  

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'variant', 'quantity')  
    search_fields = ('cart__user__email', 'variant__product__name')  
    list_filter = ('cart__created_at',)  
