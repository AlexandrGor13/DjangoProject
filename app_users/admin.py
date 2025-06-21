from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Регистрация пользователей с использованием встроенного интерфейса управления пользователями"""
    list_display = ['username', 'first_name', 'last_name', 'email', 'phone_number']
    search_fields = ['first_name', 'last_name', 'email']
