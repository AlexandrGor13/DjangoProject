from django.db import models
from django.utils.translation import gettext_lazy as get_txt


class Order(models.Model):
    """Заказ"""
    user = models.ForeignKey('app_users.User', on_delete=models.PROTECT)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=50, choices=[
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ])
    shipping_address = models.ForeignKey('DeliveryAddress', on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now_add=True)
    shipped_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = get_txt('Заказ')
        verbose_name_plural = get_txt('Заказы')

    def __str__(self):
        return f'Order #{self.pk}'


class OrderItem(models.Model):
    """Позиция заказа"""
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('app_shop.Product', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = get_txt('Элемент заказа')
        verbose_name_plural = get_txt('Элементы заказа')

    def __str__(self):
        return f'{self.product} x {self.quantity}'

    @property
    def total_price(self):
        """
        Вычисляет полную стоимость текущего товара в заказе
        """
        return format(self.quantity * self.unit_price * (1 - self.discount / 100), '.2f')


class DeliveryAddress(models.Model):
    """Адрес доставки"""
    user = models.ForeignKey('app_users.User', on_delete=models.CASCADE)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name = get_txt('Адрес доставки')
        verbose_name_plural = get_txt('Адреса доставки')

    def __str__(self):
        return f'{self.address_line}, {self.city}, {self.country}'


class Payment(models.Model):
    """Платёж"""
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, choices=[
        ('card', 'Card'),
        ('cash', 'Cash'),
        ('paypal', 'PayPal'),
    ])
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, choices=[
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('canceled', 'Canceled'),
    ])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = get_txt('Платёж')
        verbose_name_plural = get_txt('Платежи')

    def __str__(self):
        return f'Оплата за заказ #{self.order.pk}'
