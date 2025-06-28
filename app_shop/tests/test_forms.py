import pytest
from app_shop.forms import SetCaregoryForm


@pytest.mark.django_db
def test_category_form_valid(test_category):
    form_data = {
        "category": test_category,
    }

    form = SetCaregoryForm(data=form_data)
    assert form.is_valid()

    cleaned_data = form.cleaned_data
    assert cleaned_data["category"] == form_data["category"]
