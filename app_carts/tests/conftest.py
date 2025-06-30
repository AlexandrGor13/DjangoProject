import pytest

from app_carts.models import CartItem, Cart
from app_shop.models import Product, Category
from app_users.models import User


@pytest.fixture
def quantity():
    return 100


@pytest.fixture
def user():
    return User.objects.create_user(
        username="username", email="email", password="password", first_name="first_name"
    )


@pytest.fixture
def category():
    return Category.objects.create(name="Тестовая категория", slug="test")


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
def cart(user, cart_item):
    cart = Cart.objects.create(user=user)
    cart.items.add(cart_item)
    return cart


@pytest.fixture
def cart_item(product):
    return CartItem.objects.create(
        product=product,
        quantity=20,
    )
