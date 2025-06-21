from django.contrib import admin
from .models import (
    Category,
    Product,
    Review,
)


# Администрирование категорий товаров
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'parent_category']
    search_fields = ['name']


# Администрирование продуктов
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'specifications', 'price', 'discount', 'stock_quantity', 'is_active', 'category']
    list_filter = ['is_active', 'category']
    search_fields = ['title', 'description', 'price', 'discount']


# Административная регистрация модели Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'comment', 'created_at')  # Поля для отображения в списке
    search_fields = ('user__username', 'product__title', 'comment')  # Поиск по пользователям, продуктам и комментариям
    list_filter = ('rating', 'created_at')  # Фильтр по оценке и дате отзыва
    readonly_fields = ('created_at',)  # Дата создания отзыва доступна только для просмотра
