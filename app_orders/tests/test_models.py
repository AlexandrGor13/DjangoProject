import pytest
from app_orders.models import Order, OrderItem, Payment, DeliveryAddress


@pytest.mark.django_db
def test_address_creation(address):
    assert DeliveryAddress.objects.count() == 1
    assert address.state == "Тестовый регион"
    assert (
        str(address)
        == "Тестовая адресная строка, Тестовый населенный пункт, Тестовая страна"
    )


@pytest.mark.django_db
def test_order_creation(order):
    assert Order.objects.count() == 1
    assert order.status == "На погрузке"
    assert str(order) == "Order #1"


@pytest.mark.django_db
def test_order_item_creation(order_item):
    assert OrderItem.objects.count() == 1
    assert order_item.unit_price == 125
    assert order_item.order.status == "На погрузке"


@pytest.mark.django_db
def test_payment_creation(payment):
    assert Payment.objects.count() == 1
    assert payment.amount == 20
    assert payment.status == "pending"
