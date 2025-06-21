from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth import login

from app_carts.cart import get_cart, remove_from_cart
from app_orders.forms import DeliveryAddressForm
from app_orders.delivery import get_address, create_address
from app_orders.order import create_order, get_last_order, get_items_by_order
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
            if request.method == 'POST':
                if self.form_signup.is_valid():
                    username = self.form.cleaned_data.get('username')
                    email = self.form.cleaned_data.get('email')
                    password = self.form.cleaned_data.get('password')
                    password2 = self.form.cleaned_data.get('password2')
                    if password == password2:
                        user = create_user(username=username, email=email, password=password)
                        if user:
                            login(request, user)
            return render(request, 'app_orders/order_detail.html',context=self.get_context_data(**kwargs))

        return render(request,self.template_name,context=self.get_context_data(**kwargs))

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
        return render(request,self.template_name,context=self.get_context_data(**kwargs))

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
    template_name = 'app_orders/orders_list.html'
    form_delivery = DeliveryAddressForm()

    def get_context_data(self, **kwargs):
        last_order = get_last_order(self.request)

        context = super().get_context_data(**kwargs)
        context['form_delivery'] = self.form_delivery
        context['address'] = get_address(self.request)
        context['last_order'] = get_last_order(self.request)
        return context
