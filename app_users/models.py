from django.db import models
from django.utils.translation import gettext_lazy as get_txt
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Модель пользователя"""
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='%(app_label)s_%(class)s_groups',
        blank=True,
    )
    class Meta:
        verbose_name = get_txt('Пользователь')
        verbose_name_plural = get_txt('Пользователи')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
