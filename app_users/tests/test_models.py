import pytest
from app_users.models import User


@pytest.mark.django_db
def test_user_creation(user2, username):
    assert User.objects.count() == 1
    assert user2.username == username
    assert str(user2) == f"{user2.first_name} {user2.last_name}"
