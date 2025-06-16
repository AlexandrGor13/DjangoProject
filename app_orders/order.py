from app_orders.delivery import get_address
from app_users.user import get_current_user
from app_carts.cart import get_cart
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
        total_amount += item.quantity * item.product.price
        order_items = OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.price
            )
    order.total_amount = total_amount
    order.save()
