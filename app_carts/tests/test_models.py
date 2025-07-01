import pytest

from app_carts.models import Cart, CartItem


@pytest.mark.django_db
def test_cart_creation(cart):
    assert Cart.objects.count() == 1
    assert cart.user.username == "username"
    assert str(cart) == "Корзина покупок first_name "


@pytest.mark.django_db
def test_cart_item_creation(cart_item):
    assert CartItem.objects.count() == 1
    assert cart_item.quantity == 20
    assert cart_item.product.title == "Тестовый товар"
