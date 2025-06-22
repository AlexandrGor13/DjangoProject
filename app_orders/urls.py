from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.OrderFromCartView.as_view(), name='order_from_cart'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>', views.OrderView.as_view(), name='order_detail'),
    path('order/payment/', views.OrderPaymentView.as_view(), name='order_payment'),
    path('order/payment/status/', views.PaymentStatusView.as_view(), name='payment_status'),
]