from app_orders.delivery import get_address
from app_users.user import get_current_user
from app_carts.cart import get_cart, clear_cart
from app_orders.models import OrderItem, Order, DeliveryAddress


def create_order(request):
    current_user = get_current_user(request)
    cart = get_cart(request)
    total_amount = 0
    order = Order.objects.create(
        user=current_user,
        total_amount=0,
        payment_status='pending',
        shipping_address=get_address(request),
    )
    for item in cart.items.all():
        total_amount += item.quantity * item.product.price * (1 - item.product.discount/100)
        order_items = OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.price,
                discount=item.product.discount,
            )
        order_items.save()
    order.total_amount = total_amount
    order.save()
    clear_cart(request)


def get_orders(request):
    current_user = get_current_user(request)
    order = Order.objects.filter(user=current_user).all()
    if order:
        return order
    else:
        return None


def get_last_order(request):
    order = get_orders(request)
    if order:
        last_order = order.order_by('-order_date').first()
        return last_order
    else:
        return None


def get_items_by_order(current_order: Order):
    return OrderItem.objects.filter(order=current_order).all()


def move_order(request, user):
    current_user = get_current_user(request)
    order = get_last_order(request)
    order.user = user
    order.save()
    address = get_address(request)
    address.user = user
    address.save()
    current_user.delete()