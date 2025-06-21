from django.db import models
from django.utils.translation import gettext_lazy as get_txt


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
        return format(self.quantity * self.product.price * (1 - self.product.discount / 100), '.2f')


class Cart(models.Model):
    """Корзина покупок"""
    user = models.OneToOneField('app_users.User', on_delete=models.CASCADE)
    items = models.ManyToManyField('CartItem')

    class Meta:
        verbose_name = get_txt('Корзина покупок')
        verbose_name_plural = get_txt('Корзины покупок')

    def get_total_price(self):
        return format(
            sum([item.product.price * (1 - item.product.discount / 100) * item.quantity for item in self.items.all()]),
            '.2f')

    def __str__(self):
        return f'Корзина покупок {self.user}'
