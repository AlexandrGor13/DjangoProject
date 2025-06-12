from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.contrib import messages

# from .forms import ProductModelForm
from .models import Product, Category

def index(request):
    return render(request, "shop_app/index.html")


class AboutView(TemplateView):
    template_name = 'shop_app/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О нас'
        context['content'] = 'Добро пожаловать на наш сайт'
        return context


def product_list(request):
    """Представление для отображения списка товаров"""
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {"categories": categories, "products": products}
    return render(request, "shop_app/product_list.html", context=context)



class ProductDetailView(DetailView):
    """Представление для отображения деталей товара"""
    model = Product
    template_name = 'shop_app/product_detail.html'
    context_object_name = 'product'

    # def get(self, request, *args, **kwargs):
    #     product = self.get_object()
    #     return super().get(request, *args, **kwargs)

def category_list(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "shop_app/category_list.html", context=context)