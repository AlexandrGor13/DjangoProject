from django.contrib import admin
from .models import (
    Category,
    Product,
    Review,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Администрирование категорий товаров"""

    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "parent_category"]
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Администрирование продуктов"""

    list_display = [
        "title",
        "specifications",
        "price",
        "discount",
        "stock_quantity",
        "is_active",
        "category",
    ]
    list_filter = ["is_active", "category"]
    search_fields = ["title", "description", "price", "discount"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Административная регистрация модели Review"""

    list_display = (
        "user",
        "product",
        "rating",
        "comment",
        "created_at",
    )
    search_fields = (
        "user__username",
        "product__title",
        "comment",
    )
    list_filter = ("rating", "created_at")
    readonly_fields = ("created_at",)
