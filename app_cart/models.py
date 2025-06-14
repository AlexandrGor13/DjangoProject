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

    @property
    def availability(self):
        """
        """
        return True if self.quantity <= self.product.stock_quantity else False


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

    # @property
    # def cart(self):
    #     return {item.product.id: item.quantity for item in self.items.all()}
    #
    #
    # def add(self, product_id: int, quantity=1) -> None:
    #     """
    #     Добавление товара
    #     """
    #     product_id = str(product_id)
    #
    #     if product_id not in self.cart:
    #         self.cart.update({product_id: {'quantity': 1}})
    #     else:
    #         self.cart[product_id]['quantity'] += quantity
    #
    #     self.cart[product_id]['quantity'] = quantity
    #
    #     self.save()



class CurrentCart():
    """Корзина с товарами для покупки"""
    def __init__(self, request: HttpRequest):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def save(self):
        """ Сохранение изменений в корзине в сессии"""
        self.session.modified = True

    def add(self, product_id: UUID, quantity=1, updated=False) -> None:
        """
        Добавление товара
        """
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart.update({product_id: {'quantity': 1}})
        else:
            self.cart[product_id]['quantity'] += quantity

        if updated:
            self.cart[product_id]['quantity'] = quantity

        self.save()

    def remove(self, product_id: UUID) -> None:
        """
        Удаление 1 товара из корзины.
        """
        product_id_str = str(product_id)

        if product_id_str in self.cart.keys():
            if self.cart[product_id_str]['quantity'] <= 1:
                self.delete_all(product_id)
            else:
                self.cart[product_id_str]['quantity'] -= 1
                self.save()

    def delete_all(self, product_id: UUID) -> None:
        """
        Удаление товара из корзины.
        """
        product_id = str(product_id)

        if product_id in self.cart.keys():
            self.cart.pop(product_id)
            self.save()

    def clear(self):
        """Очистка корзины"""
        self.session.pop(settings.CART_SESSION_ID)
        self.save()

    def __iter__(self) -> CartItem:
        products = Product.objects.filter(product_id__in=self.cart.keys())

        for product in products:
            quantity = self.cart.get(str(product.product_id)).get('quantity')
            yield CartItem(product=product,
                           quantity=quantity)

    def __len__(self) -> int:
        """
        Количество товаров в корзине.
        """
        return len(self.cart.keys())

    def get_total_price(self) -> Decimal:
        """
        Получение общей стоимости товаров.
        """
        return sum([item.total_price for item in self])

    def get_quantity(self, product_id: UUID) -> int:
        """
        Возвращает количество товаров по product_id
        """
        data_product = self.cart.get(str(product_id))
        if data_product:
            return data_product.get('quantity')
        return 0
