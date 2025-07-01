import pytest
from app_shop.models import Product, Category


@pytest.fixture
def test_category():
    return "Тестовая категория"


@pytest.fixture
def category(test_category):
    return Category.objects.create(name=test_category, slug="test")


@pytest.fixture
def product(category):
    return Product.objects.create(
        title="Тестовый товар",
        specifications="Характеристики товара",
        description="Описание тестового товара",
        price=10.1,
        category=category,
        stock_quantity=100,
    )


@pytest.fixture
def product2(category):
    return Product.objects.create(
        title="Другой тестовый товар",
        specifications="Характеристики товара",
        description="Описание другого тестового товара",
        price=50.5,
        category=category,
    )
