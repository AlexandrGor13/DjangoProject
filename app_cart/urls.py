from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart_detail'),
    # path('cart/<int:pk>/add/', views.cart_add, name='cart_add'),
    # path('cart/<int:pk>/remove/', views.cart_remove, name='cart_remove'),
]