from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import SignUpForm, LoginForm, CartAddProductForm
from .models import Product, Category, User, ShoppingCart, CartItem

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'shop_app/signup.html', {'form': form})

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    return render(request, 'shop_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def index(request):
    return render(request, "shop_app/index.html")


class AboutView(TemplateView):
    template_name = 'shop_app/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О нас'
        context['content'] = 'Добро пожаловать на наш сайт'
        return context


class ProductView(TemplateView):
    """Представление для отображения товара"""
    template_name = 'shop_app/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    """Представление для отображения деталей товара"""
    model = Product
    template_name = 'shop_app/product_detail.html'
    context_object_name = 'product'


class CategoryView(ListView):
    """Представление для отображения категорий"""
    model = Category
    template_name = 'shop_app/category_list.html'
    context_object_name = 'categories'
#
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
    model = ShoppingCart
    template_name = 'shop_app/cart_detail.html'
    context_object_name = 'cart'