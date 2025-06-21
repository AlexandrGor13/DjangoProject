from .models import User
from app_carts.models import Cart


def get_current_user(request):
    if not request.session.session_key:
        request.session.create()
    return User.objects.get(id=request.user.id) if request.user.is_authenticated else get_anonymous_user(request)


def get_anonymous_user(request):
    if not request.session.session_key:
        request.session.create()
    anonymous_user = User.objects.filter(username=request.session.session_key).first()
    if not anonymous_user:
        anonymous_user = User.objects.create(
            username=request.session.session_key,
            first_name='anonymous',
            email='o@o',
            password='********',
        )
        anonymous_user.save()
    cart = Cart.objects.filter(user=anonymous_user).first()
    if not cart:
        cart = Cart.objects.create(user=anonymous_user)
    cart.save()
    return anonymous_user


def create_user(username, email, password):
    user = User.objects.create(
        username=username,
        email=email,
        password=password
    )
    user.save()
    return user
