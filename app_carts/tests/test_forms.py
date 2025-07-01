import pytest
from app_carts.forms import CartAddProductForm


@pytest.mark.django_db
def test_cart_form_valid(quantity, product):
    form_data = {
        "quantity": quantity,
        "product": product.id,
    }

    form = CartAddProductForm(data=form_data)
    assert form.is_valid()

    cleaned_data = form.cleaned_data
    assert cleaned_data["quantity"] == form_data["quantity"]
