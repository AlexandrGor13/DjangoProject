from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.OrderFromCartView.as_view(), name='order_from_cart'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>', views.OrderView.as_view(), name='order_detail'),
    path('order/payment/', views.OrderPaymentView.as_view(), name='order_payment'),

    # path('', lambda request: HttpResponseRedirect('/admin/')),  # Главная страница переадресует в админку
    path('create_payment/<int:order_id>/', views.create_payment),
    path('payment_success/', views.payment_success),
    path('check_payment_status/', views.check_payment_status),
]