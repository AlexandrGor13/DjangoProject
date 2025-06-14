from http import HTTPStatus

from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Product, Category
from app_cart.models import Cart
from app_cart.forms import CartAddProductForm


def index(request):
    return render(request, "app_shop/index.html")


class AboutView(TemplateView):
    template_name = 'app_shop/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О нас'
        context['content'] = 'Добро пожаловать на наш сайт'
        return context


class ProductView(TemplateView):
    """Представление для отображения товара"""
    template_name = 'app_shop/product_list.html'
    success_url = reverse_lazy('cart_detail')
    form = CartAddProductForm()

    def post(self, request, *args, **kwargs):
        print(request.POST.get('quantity'))
        print(request.POST.get('product'))
        return render(request, 'app_shop/product_list.html')

    def form_valid(self, form):
        # Прочитать данные из `form.cleaned_data`
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['categories'] = Category.objects.all()
        context['form'] = self.form
        return context


class ProductDetailView(DetailView):
    """Представление для отображения деталей товара"""
    model = Product
    template_name = 'app_shop/product_detail.html'
    context_object_name = 'product'


class CategoryView(ListView):
    """Представление для отображения категорий"""
    model = Category
    template_name = 'app_shop/category_list.html'
    context_object_name = 'categories'

# @require_POST
# def cart_add(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(product=product,
#                  quantity=cd['quantity'],
#                  update_quantity=cd['update'])
#     return redirect('shop_app/cart_detail.html')
#
# def cart_remove(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     cart.remove(product)
#     return redirect('shop_app/cart_detail.html')

class CartView(DetailView):
    """Представление для отображения категорий"""
    model = Cart
    template_name = 'app_shop/cart_detail.html'
    context_object_name = 'cart'