from django.db import models
from django.utils.translation import gettext_lazy as get_txt

from decimal import Decimal
from uuid import UUID

from django.conf import settings
from django.http import HttpRequest

from app_shop.models import Product
from app_users.models import User


class CartItem(models.Model):
    """Элемент корзины"""
    product = models.ForeignKey('app_shop.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")

    class Meta:
        verbose_name = "Позиция корзины"
        verbose_name_plural = "Позиции корзины"

    def __str__(self):
        return f'{self.product} x {self.quantity}'

    @property
    def total_price(self):
        """
        Вычисляет полную стоимость текущего товара в корзине
        """
        return self.quantity * self.product.price



class Cart(models.Model):
    """Корзина покупок"""
    user = models.OneToOneField('app_users.User', on_delete=models.CASCADE)
    items = models.ManyToManyField('CartItem')

    class Meta:
        verbose_name = get_txt('Корзина покупок')
        verbose_name_plural = get_txt('Корзины покупок')

    def get_total_price(self):
        return sum([item.product.price * item.quantity for item in self.items.all()])

    def __str__(self):
        return f'Корзина покупок {self.user}'


