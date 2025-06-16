from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect

from .models import Product, Category
from .forms import SetCaregoryForm
from app_carts.forms import CartAddProductForm
from app_carts.models import Cart
from app_carts.cart import add_to_cart


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
    form_cart = CartAddProductForm()
    form_category = SetCaregoryForm()
    category = None

    def post(self, request, *args, **kwargs):
        if request.POST.get('product') and request.POST.get('quantity'):
            add_to_cart(request)
            return redirect('cart_detail')
        else:
            self.category = request.POST.get('category')
            return render(request, self.template_name, context=self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all() if not self.category else Product.objects.filter(
            category=Category.objects.get(name=self.category))
        context['categories'] = Category.objects.all()
        context['form_cart'] = self.form_cart
        context['form_category'] = self.form_category
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


class CartView(DetailView):
    """Представление для отображения категорий"""
    model = Cart
    template_name = 'app_shop/cart_detail.html'
    context_object_name = 'cart'
