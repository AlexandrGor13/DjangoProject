from django.contrib import admin
from .models import (
    Order,
    OrderItem,
    DeliveryAddress,
    Payment,
)

# Инлайн отображение позиций заказов
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


# Управление заказами
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'user', 'total_amount', 'payment_status', 'order_date']
    list_filter = ['payment_status']
    search_fields = ['user__first_name', 'user__last_name']
    readonly_fields = ['order_date', 'shipped_date', 'completed_date']


# Административная регистрация модели DeliveryAddress
@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'address_line1', 'city', 'state', 'zip_code', 'country', 'default')  # Поля для отображения в списке
    search_fields = ('address_line1', 'city', 'state', 'country')  # Поисковые поля
    list_filter = ('default',)  # Возможность фильтрации по полю default
    raw_id_fields = ('user',)  # Поле связи с пользователем для удобства выборки большого числа пользователей


# Административная регистрация модели Payment
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'method', 'status', 'timestamp')  # Поля для отображения в списке
    search_fields = ('transaction_id', 'order__id')  # Поиск по номеру транзакции и ID заказа
    list_filter = ('status', 'method')  # Фильтры по статусу и типу платежа
    readonly_fields = ('timestamp',)  # Только для чтения (не изменяется вручную)
