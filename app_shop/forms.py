from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category

class CartAddProductForm(forms.Form):
    """Форма для изменения количества товаров в корзине"""
    quantity = forms.IntegerField()
    product = forms.IntegerField()

class SetCaregoryForm(forms.Form):
    """"""
    caregory = forms.CharField()