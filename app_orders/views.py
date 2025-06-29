from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth import login

from app_carts.cart import get_cart, remove_from_cart
from app_orders.forms import DeliveryAddressForm
from app_orders.delivery import get_address, create_address
from app_orders.models import Order, Payment
from app_orders.order import (
    create_order,
    get_last_order,
    get_items_by_order,
    move_order,
    get_orders,
)
from app_orders.payment import create_order_payment, get_status_payment
from app_users.forms import SignUpForm
from app_users.user import get_current_user, create_user


class OrderFromCartView(TemplateView):
    """Отображение заказа из корзины"""

    template_name = "app_orders/order_from_cart.html"

    form_delivery = DeliveryAddressForm()
    form_signup = SignUpForm()

    def post(self, request, *args, **kwargs):
        if request.POST.get("product"):
            remove_from_cart(request)
        else:
            create_address(request)
            create_order(request)
            form_signup = SignUpForm(request.POST)
            if get_current_user(request).first_name == "anonymous":
                if form_signup.is_valid():
                    username = form_signup.cleaned_data.get("username")
                    email = form_signup.cleaned_data.get("email")
                    password = form_signup.cleaned_data.get("password")
                    password2 = form_signup.cleaned_data.get("password2")
                    if password == password2:
                        user = create_user(
                            username=username, email=email, password=password
                        )
                        if user:
                            move_order(request, user)
                            login(request, user)
                else:
                    return render(
                        request,
                        self.template_name,
                        context=self.get_context_data(**kwargs),
                    )
            return redirect("/order/payment", context=self.get_context_data(**kwargs))

        return render(
            request, self.template_name, context=self.get_context_data(**kwargs)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = get_cart(self.request)
        context["form_delivery"] = self.form_delivery
        context["form_signup"] = self.form_signup
        context["address"] = get_address(self.request)
        context["order"] = get_last_order(self.request)
        context["current_user"] = get_current_user(self.request)
        context["items"] = get_items_by_order(context["order"])
        return context


class OrderPaymentView(TemplateView):
    """Отображение заказа из корзины"""

    template_name = "app_orders/order_payment.html"

    def post(self, request, *args, **kwargs):
        payment_url = create_order_payment(request)
        return redirect(payment_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["address"] = get_address(self.request)
        context["order"] = get_last_order(self.request)
        context["items"] = get_items_by_order(context["order"])
        return context


class OrderView(DetailView):
    """Отображение заказа"""

    model = Order
    template_name = "app_orders/order_detail.html"
    context_object_name = "order"

    def get_object(self):
        obj = super().get_object()
        obj = {"order": obj, "items": get_items_by_order(obj)}
        return obj


class OrderListView(ListView):
    """Отображение списка заказов"""

    model = Order
    template_name = "app_orders/orders_list.html"
    context_object_name = "orders"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = get_orders(self.request)
        if orders:
            orders = {order: get_items_by_order(order) for order in orders}
        context["orders"] = orders
        return context


class PaymentStatusView(TemplateView):
    """Отображение успешной оплаты"""

    template_name = "app_orders/payment_status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.request.GET.get("id")
        payment = Payment.objects.get(id=id)
        context["status"] = get_status_payment(payment)
        return context
