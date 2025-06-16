from django import forms


class CartAddProductForm(forms.Form):
    """Форма для изменения количества товаров в корзине"""
    quantity = forms.IntegerField()
    product = forms.IntegerField()
