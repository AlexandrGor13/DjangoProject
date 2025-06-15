from .models import Cart, CartItem
from app_shop.models import Product
from app_users.models import User


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


def add_to_cart(request):
    if not request.session.session_key:
        request.session.create()
    product_id = int(request.POST.get('product'))
    quantity = int(request.POST.get('quantity'))
    current_product = Product.objects.get(id=product_id)
    current_user = get_current_user(request)
    current_cart = Cart.objects.filter(user=current_user).first()
    current_cart_item = CartItem.objects.create(product=current_product, quantity=quantity)
    current_cart_item.save()
    if not current_cart:
        current_cart = Cart.objects.create(user=current_user)
        current_cart.items.set([current_cart_item])
    else:
        if current_cart.items.filter(product=current_product).count():
            cart_item = current_cart.items.get(product=current_product)
            cart_item.quantity += quantity
            cart_item.save(update_fields=["quantity"])
        else:
            print(current_cart.items.exists())
            current_cart_items = [current_cart.items.get()] if current_cart.items.exists() else []
            if current_cart.items.exists():
                print(current_cart.items.get())
            current_cart.items.set(current_cart_items + [current_cart_item])
    current_cart.save()


def remove_from_cart(request):
    product_id = int(request.POST.get('product'))
    current_product = Product.objects.get(id=product_id)
    cart = get_cart(request)
    cart.items.filter(product=current_product).delete()


def move_cart(request, session_key):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        cart = Cart.objects.filter(user=current_user).first()
        anonymous_user = User.objects.filter(username=session_key).first()
        if anonymous_user:
            cart_anonymous_user = Cart.objects.get(user=anonymous_user)
            if not cart or not cart.items.count():
                cart_anonymous_user.user = current_user
                cart_anonymous_user.save(update_fields=["user"])
                anonymous_user.delete()


def get_cart(request):
    current_user = get_current_user(request)
    cart = Cart.objects.filter(user=current_user).first()
    if not cart:
        cart = Cart.objects.create(user=current_user)
        cart.save()
    return cart


def get_current_user(request):
    if not request.session.session_key:
        request.session.create()
    return User.objects.get(id=request.user.id) if request.user.is_authenticated else get_anonymous_user(request)
