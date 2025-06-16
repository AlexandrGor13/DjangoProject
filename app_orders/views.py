from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from app_carts.cart import get_cart, remove_from_cart
from app_orders.forms import DeliveryAddressForm
from app_orders.delivery import get_address, create_address
from app_orders.order import create_order


class OrderView(TemplateView):
    """Отображение заказа из корзины"""
    template_name = 'app_orders/order_detail.html'

    form_delivery = DeliveryAddressForm()

    def post(self, request, *args, **kwargs):
        if request.POST.get('product'):
            remove_from_cart(request)
        else:
            create_address(request)
            create_order(request)

        return render(request,self.template_name,context=self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = get_cart(self.request)
        context['form_delivery'] = self.form_delivery
        context['address'] = get_address(self.request)
        return context
