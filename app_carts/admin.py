from django.contrib import admin
from .models import CartItem, Cart


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Элементы корзин"""
    list_display = ['product', 'quantity', 'added_at']
    search_fields = ['product__title']
    readonly_fields = ['added_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Корзины покупателей"""
    filter_horizontal = ['items']
    list_display = ['user']
