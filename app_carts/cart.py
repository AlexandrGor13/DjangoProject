from .models import Cart, CartItem
from app_shop.models import Product
from app_users.models import User
from app_users.user import get_current_user, get_anonymous_user


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
    elif not current_cart.items:
        current_cart.items = current_cart_item
    else:
        if current_cart.items.filter(product=current_product).count():
            cart_item = current_cart.items.get(product=current_product)
            cart_item.quantity += quantity
            cart_item.save(update_fields=["quantity"])
        else:
            current_cart.items.add(current_cart_item)
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


def clear_cart(request):
    current_user = get_current_user(request)
    cart = Cart.objects.filter(user=current_user).first()
    if cart:
        for item in cart.items.all():
            item.delete()
        return True
    return False