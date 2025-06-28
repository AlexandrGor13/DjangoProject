import pytest
from app_users.forms import SignUpForm, LoginForm


@pytest.mark.django_db
def test_sign_form_valid(username, email, password):
    form_data = {
        "username": username,
        "email": email,
        "password": password,
        "password2": password,
    }
    form = SignUpForm(data=form_data)
    assert form.is_valid()

    cleaned_data = form.cleaned_data
    assert cleaned_data["password"] == form_data["password"]


@pytest.mark.django_db
def test_login_form_valid(username, password2, user1):
    form_data = {
        "username": username,
        "password": password2,
    }
    form = LoginForm(data=form_data)
    assert form.is_valid()

    cleaned_data = form.cleaned_data
    assert cleaned_data["password"] == form_data["password"]
    assert cleaned_data["username"] == form_data["username"]
