from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

from app_cart.models import Cart
from app_cart.forms import CartAddProductForm
from app_cart.services.mixins_for_cart import (
    GetContextTotalPriceCartMixin,
    CartRequestMixin,
    NextURLRequestMixin
)

# from app_categories.services.navi_categories_list import NaviCategoriesList


class CartView(TemplateView):
    """Отображение корзины"""
    template_name = 'app_cart/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        cart = self.request.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.request.session[settings.CART_SESSION_ID] = {}
        context.update({'cart': cart})
        # context.update(NaviCategoriesList().get_context())
        # context.update(self.get_context_price_cart())
        # if self.request.user.is_authenticated:

        # print(context)
        # print(self.request.user.is_authenticated)
        # print(self.request.session.session_key)
        # print(dir(self.request.session))
        # print(self.request.session.__dict__)
        return context


class AddProductCartView(View):
    """Представление для добавления товаров со страниц с товарами"""

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        self.cart.add(product_id)
        return redirect(self.next_url)


class UpdateProductCartVIew(View, NextURLRequestMixin):
    """Представление для добавления товаров через форму"""

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cart = Cart(request)
            cart.add(product_id=product_id,
                     quantity=form.cleaned_data.get('quantity'),
                     updated=form.cleaned_data.get('update'))
        return redirect(self.next_url)


class RemoveProductCartView(View, CartRequestMixin, NextURLRequestMixin):
    """Представление для удаления 1 шт. товара из корзины"""

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        self.cart.remove(product_id)
        return redirect(self.next_url)


class DeleteAllProductCartView(View, CartRequestMixin):
    """Представление для удаления товаров из корзины"""

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        self.cart.delete_all(product_id)
        return redirect('cart')


class ClearCartView(View, CartRequestMixin):
    """Представление для очистки корзины"""

    def get(self, request, *args, **kwargs):
        self.cart.clear()
        return redirect('cart')
