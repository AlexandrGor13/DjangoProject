from django.db import models
from django.utils.translation import gettext_lazy as get_txt


class Category(models.Model):
    """Категория продуктов"""
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = get_txt('Категория')
        verbose_name_plural = get_txt('Категории')

    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар"""
    title = models.CharField(max_length=255)
    specifications = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField(default=0)
    img = models.ImageField(upload_to='./static/img', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = get_txt('Товар')
        verbose_name_plural = get_txt('Товары')

    def __str__(self):
        return f'{self.title} {self.specifications}'


class Review(models.Model):
    """Отзыв клиента"""
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey('app_users.User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[
        (1, 'Very Bad'),
        (2, 'Bad'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    ])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = get_txt('Отзыв')
        verbose_name_plural = get_txt('Отзывы')

    def __str__(self):
        return f'Отзыв {self.user} о {self.product}'
