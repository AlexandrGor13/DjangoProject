from django.contrib import admin
from .models import (
    Order,
    OrderItem,
    DeliveryAddress,
    Payment,
)


class OrderItemInline(admin.TabularInline):
    """Инлайн отображение позиций заказов"""
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Управление заказами"""
    inlines = [OrderItemInline]
    list_display = ['id', 'user', 'total_amount', 'status', 'order_date']
    search_fields = ['user__first_name', 'user__last_name']
    list_filter = ('status',)
    readonly_fields = ['order_date', 'shipped_date', 'completed_date']


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    """Административная регистрация модели DeliveryAddress"""
    list_display = ('address_line', 'city', 'state', 'zip_code', 'country', 'default')
    search_fields = ('address_line', 'city', 'state', 'country')
    list_filter = ('default',)
    raw_id_fields = ('user',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Административная регистрация модели Payment"""
    list_display = ('order', 'amount', 'status', 'timestamp')
    search_fields = ('transaction_id', 'order__id')
    list_filter = ('status',)
    readonly_fields = ('timestamp',)
