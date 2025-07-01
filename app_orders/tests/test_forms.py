import pytest
from app_orders.forms import DeliveryAddressForm


@pytest.mark.django_db
def test_address_form_valid(
    test_address_line, test_city, test_state, test_zip_code, test_country
):
    form_data = {
        "address_line": test_address_line,
        "city": test_city,
        "state": test_state,
        "zip_code": test_zip_code,
        "country": test_country,
    }

    form = DeliveryAddressForm(data=form_data)
    assert form.is_valid()

    cleaned_data = form.cleaned_data
    assert cleaned_data["address_line"] == form_data["address_line"]
