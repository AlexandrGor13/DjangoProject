from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

from .models import Cart
from .cart import get_cart, remove_from_cart
from app_shop.forms import CartAddProductForm


# from app_categories.services.navi_categories_list import NaviCategoriesList


class CartView(TemplateView):
    """Отображение корзины"""
    template_name = 'app_cart/cart_detail.html'
    form = CartAddProductForm()

    def post(self, request, *args, **kwargs):
        remove_from_cart(request)
        print(request.POST)
        return redirect('cart_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = get_cart(self.request)
        context['form'] = self.form
        return context



# class AddProductCartView(View):
#     """Представление для добавления товаров со страниц с товарами"""
#
#     def get(self, request, *args, **kwargs):
#         product_id = kwargs.get('product_id')
#         self.cart.add(product_id)
#         return redirect(self.next_url)
#
#
# class UpdateProductCartVIew(View, NextURLRequestMixin):
#     """Представление для добавления товаров через форму"""
#
#     def post(self, request, *args, **kwargs):
#         product_id = kwargs.get('product_id')
#         form = CartAddProductForm(request.POST)
#         if form.is_valid():
#             cart = Cart(request)
#             cart.add(product_id=product_id,
#                      quantity=form.cleaned_data.get('quantity'),
#                      updated=form.cleaned_data.get('update'))
#         return redirect(self.next_url)
#
#
# class RemoveProductCartView(View, CartRequestMixin, NextURLRequestMixin):
#     """Представление для удаления 1 шт. товара из корзины"""
#
#     def get(self, request, *args, **kwargs):
#         product_id = kwargs.get('product_id')
#         self.cart.remove(product_id)
#         return redirect(self.next_url)
#
#
# class DeleteAllProductCartView(View, CartRequestMixin):
#     """Представление для удаления товаров из корзины"""
#
#     def get(self, request, *args, **kwargs):
#         product_id = kwargs.get('product_id')
#         self.cart.delete_all(product_id)
#         return redirect('cart')
#
#
# class ClearCartView(View, CartRequestMixin):
#     """Представление для очистки корзины"""
#
#     def get(self, request, *args, **kwargs):
#         self.cart.clear()
#         return redirect('cart')
