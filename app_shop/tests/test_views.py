import pytest
from django.urls import reverse
from app_shop.models import Product


@pytest.mark.django_db
def test_product_list(client, product, category):
    url = reverse("products")
    response = client.get(url)

    assert response.status_code == 200

    assert product.title.encode() in response.content


@pytest.mark.django_db
def test_product_detail(client, product, category):
    url = reverse("product_detail", args=[product.id])
    response = client.get(url)

    assert response.status_code == 200

    assert product.title.encode() in response.content
    assert category.name.encode() in response.content


@pytest.mark.django_db
def test_product_filter(client, product, category):
    url = reverse("products")
    response = client.get(url, {"price": 10.1})
    assert response.status_code == 200

    assert product.title in response.content.decode("utf-8")

    low_price_product = Product.objects.create(
        title="Низкая цена",
        specifications="",
        description="Тут низкая цена",
        price=2,
        category=category,
    )
    assert low_price_product.title not in response.content.decode("utf-8")
