from django import forms

class DeliveryAddressForm(forms.Form):
    address_line1 = forms.CharField()
    address_line2 = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    zip_code = forms.CharField()
    country = forms.CharField()

#
# class AddOrderForm(forms.Form):
#     """Форма для оформления заказа"""
#     quantity = forms.IntegerField()
#     product = forms.IntegerField()
#
#     order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
#     product = models.ForeignKey('app_shop.Product', on_delete=models.PROTECT)
#     quantity = models.PositiveSmallIntegerField()
#     unit_price = models.DecimalField(max_digits=10, decimal_places=2)
#     discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
