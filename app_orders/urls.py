from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.OrderFromCartView.as_view(), name='order_from_cart'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>', views.OrderListView.as_view(), name='order_detail'),
]