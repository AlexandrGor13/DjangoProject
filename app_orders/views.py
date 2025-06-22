from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth import login

from app_carts.cart import get_cart, remove_from_cart
from app_orders.forms import DeliveryAddressForm
from app_orders.delivery import get_address, create_address
from app_orders.models import Order
from app_orders.order import create_order, get_last_order, get_items_by_order, move_order, get_orders
from app_users.forms import SignUpForm
from app_users.user import get_current_user, create_user


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
            return render(request, 'app_orders/order_detail.html', context=self.get_context_data(**kwargs))

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


class OrderView(TemplateView):
    """Отображение заказа"""
    template_name = 'app_orders/order_detail.html'
    form_delivery = DeliveryAddressForm()

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, context=self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_order = get_last_order(self.request)
        context['form_delivery'] = self.form_delivery
        context['address'] = get_address(self.request)
        context['order'] = last_order
        context['items'] = get_items_by_order(last_order)
        return context


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
