import pytest
from app_users.models import User


@pytest.fixture
def username():
    return "user"


@pytest.fixture
def email():
    return "user@example.com"


@pytest.fixture
def password():
    return "password"


@pytest.fixture
def password2():
    return "password2"


@pytest.fixture
def first_name():
    return "first_name"


@pytest.fixture
def last_name():
    return "last_name"


@pytest.fixture
def user1(username, email, password2):
    return User.objects.create_user(username=username, email=email, password=password2)


@pytest.fixture
def user2(username, email, password, first_name, last_name):
    return User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
