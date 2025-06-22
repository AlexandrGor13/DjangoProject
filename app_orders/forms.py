from django import forms

class DeliveryAddressForm(forms.Form):
    address_line = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    zip_code = forms.CharField()
    country = forms.CharField()

# class OrderPaymentForm(forms.Form):
#     method = forms.ChoiceField(choices=[
#         ('card', 'Карта'),
#         ('cash', 'Наличные'),
#         ('yookassa', 'ЮKassa'),
#     ])

