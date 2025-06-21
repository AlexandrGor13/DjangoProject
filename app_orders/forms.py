from django import forms

class DeliveryAddressForm(forms.Form):
    address_line1 = forms.CharField()
    address_line2 = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    zip_code = forms.CharField()
    country = forms.CharField()

