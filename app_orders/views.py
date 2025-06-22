from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth import login
from django.conf import settings

from yookassa import Configuration, Payment

from app_carts.cart import get_cart, remove_from_cart
from app_orders.forms import DeliveryAddressForm
from app_orders.delivery import get_address, create_address
from app_orders.models import Order, Payment as PaymentModel
from app_orders.order import create_order, get_last_order, get_items_by_order, move_order, get_orders
from app_users.forms import SignUpForm
from app_users.user import get_current_user, create_user


Configuration.account_id = settings.SHOP_ACCOUNT_ID
Configuration.secret_key = settings.SHOP_SECRET_KEY


def create_payment(request):
    try:
        order = get_last_order(request)
        payment = PaymentModel.objects.filter(order=order).first()

        if payment.status != 'pending':
            return redirect('home')  # Если заказ уже оплачен или отменён, перенаправляем обратно

        payment_data = {
            'amount': {'value': str(payment.amount), 'currency': 'RUB'},
            'confirmation': {'type': 'redirect',
                             'return_url': f'{request.scheme}://{request.get_host()}/payment_success/'},
            'capture': True,
            'description': f'Оплата заказа № {payment.order.id}',
        }

        payment = Payment.create(payment_data)

        return redirect(payment.confirmation.confirmation_url)

    except Exception as e:
        print(e)
        return redirect('home')


def payment_success(request):
    return render(request, 'app_orders/payment_success.html')


def check_payment_status(request):
    payments = Payment.list({'limit': 1})
    for payment in payments.items:
        if payment.status == 'succeeded':
            order_id = int(payment.description.split('№')[1].strip())
            try:
                order = Order.objects.get(id=order_id)
                order.payment_status = 'paid'
                order.save()
            except Order.DoesNotExist:
                pass

    return redirect('home')

class OrderFromCartView(TemplateView):
    """Отображение заказа из корзины"""
    template_name = 'app_orders/order_from_cart.html'

    form_delivery = DeliveryAddressForm()
    form_signup = SignUpForm()

    def post(self, request, *args, **kwargs):
        if request.POST.get('product'):
            remove_from_cart(request)
        else:
            create_address(request)
            create_order(request)
            form_signup = SignUpForm(request.POST)
            if get_current_user(request).first_name == "anonymous":
                if form_signup.is_valid():
                    username = form_signup.cleaned_data.get('username')
                    email = form_signup.cleaned_data.get('email')
                    password = form_signup.cleaned_data.get('password')
                    password2 = form_signup.cleaned_data.get('password2')
                    if password == password2:
                        user = create_user(username=username, email=email, password=password)
                        if user:
                            move_order(request, user)
                            login(request, user)
                else:
                    return render(request, self.template_name, context=self.get_context_data(**kwargs))
            return render(request, 'app_orders/order_payment.html', context=self.get_context_data(**kwargs))

        return render(request, self.template_name, context=self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_order = get_last_order(self.request)
        context['cart'] = get_cart(self.request)
        context['form_delivery'] = self.form_delivery
        context['form_signup'] = self.form_signup
        context['address'] = get_address(self.request)
        context['order'] = last_order
        context['current_user'] = get_current_user(self.request)
        context['items'] = get_items_by_order(last_order)
        return context


class OrderPaymentView(TemplateView):
    """Отображение заказа из корзины"""
    template_name = 'app_orders/order_payment.html'

    form_delivery = DeliveryAddressForm()
    form_signup = SignUpForm()

    def post(self, request, *args, **kwargs):
        create_address(request)
        create_order(request)
        form_signup = SignUpForm(request.POST)
        if get_current_user(request).first_name == "anonymous":
            if form_signup.is_valid():
                username = form_signup.cleaned_data.get('username')
                email = form_signup.cleaned_data.get('email')
                password = form_signup.cleaned_data.get('password')
                password2 = form_signup.cleaned_data.get('password2')
                if password == password2:
                    user = create_user(username=username, email=email, password=password)
                    if user:
                        move_order(request, user)
                        login(request, user)

        return render(request, self.template_name, context=self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_order = get_last_order(self.request)
        context['cart'] = get_cart(self.request)
        context['form_delivery'] = self.form_delivery
        context['form_signup'] = self.form_signup
        context['address'] = get_address(self.request)
        context['order'] = last_order
        context['current_user'] = get_current_user(self.request)
        context['items'] = get_items_by_order(last_order)
        return context


class OrderView(DetailView):
    """Отображение заказа"""
    model = Order
    template_name = 'app_orders/order_detail.html'
    context_object_name = 'order'

    def get_object(self):
        obj = super().get_object()
        obj = {"order": obj, "items": get_items_by_order(obj)}
        return obj



class OrderListView(ListView):
    """Отображение списка заказов"""
    model = Order
    template_name = 'app_orders/orders_list.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = {order: get_items_by_order(order) for order in get_orders(self.request)}
        context['orders'] = orders
        return context
