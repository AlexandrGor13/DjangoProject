from django.views.generic import TemplateView
from django.shortcuts import render

from .cart import get_cart, remove_from_cart
from .forms import CartAddProductForm


class CartView(TemplateView):
    """Отображение корзины"""
    template_name = 'app_carts/cart_detail.html'
    form = CartAddProductForm()

    def post(self, request, *args, **kwargs):
        remove_from_cart(request)
        return render(request, self.template_name, context=self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = get_cart(self.request)
        context['form'] = self.form
        return context
