from django.contrib import admin
from .models import CartItem, Cart


# Элементы корзин
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'added_at']
    search_fields = ['product__title']
    readonly_fields = ['added_at']


# Корзины покупателей
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    filter_horizontal = ['items']  # Удобнее выбирать элементы корзины
    list_display = ['user']
