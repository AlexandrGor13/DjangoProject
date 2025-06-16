from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path('about/', views.AboutView.as_view(), name='about'),
    path('products/', views.ProductView.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
]
