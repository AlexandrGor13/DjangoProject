import pytest
from app_orders.models import Order, OrderItem, Payment, DeliveryAddress
from app_shop.models import Product, Category
from app_users.models import User


@pytest.fixture
def user():
    return User.objects.create_user(
        username="username", email="email", password="password"
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
def test_address_line():
    return "Тестовая адресная строка"


@pytest.fixture
def test_city():
    return "Тестовый населенный пункт"


@pytest.fixture
def test_state():
    return "Тестовый регион"


@pytest.fixture
def test_zip_code():
    return "Тестовый"


@pytest.fixture
def test_country():
    return "Тестовая страна"


@pytest.fixture
def address(
    user, test_address_line, test_city, test_state, test_zip_code, test_country
):
    return DeliveryAddress.objects.create(
        user=user,
        address_line=test_address_line,
        city=test_city,
        state=test_state,
        zip_code=test_zip_code,
        country=test_country,
    )


@pytest.fixture
def order(user, address):
    return Order.objects.create(
        user=user,
        total_amount=1000.50,
        shipping_address=address,
        status="На погрузке",
    )


@pytest.fixture
def order_item(order, product):
    return OrderItem.objects.create(
        order=order,
        product=product,
        quantity=20,
        unit_price=125,
        discount=0,
    )


@pytest.fixture
def payment(order):
    return Payment.objects.create(
        order=order,
        amount=20,
    )
