from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category

#
#
# class ProductForm(forms.Form):
#     title = forms.CharField(
#         max_length=100,
#         label='Название',
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название продукта'})
#
#     )
#     specifications = forms.CharField(
#         max_length=150,
#         label='Характеристики',
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите характеристики продукта'})
#
#     )
#     description = forms.CharField(
#         label='Описание',
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Введите описание продукта'})
#
#     )
#     price = forms.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         label='Цена',
#         widget=forms.NumberInput(attrs={'class': 'form-control'})
#
#     )
#
#     category = forms.ModelChoiceField(
#         queryset=Category.objects.all(),
#         label='Категория',
#         empty_label='Выберите категорию',
#         widget = forms.Select(attrs={'class': 'form-control'})
#     )
#
# class ProductModelForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ["name", "specifications", "price", "description", "category"]
#         labels = {
#             'name': 'Название',
#             "specifications": "Характеристики",
#             'price': 'Цена',
#             'description': 'Описание',
#             'category': 'Категория',
#         }
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название продукта'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Введите описание продукта'}),
#             'price': forms.NumberInput(attrs={'class': 'form-control'}),
#             'category': forms.Select(attrs={'class': 'form-control'}),
#         }
#
#     def clean_name(self):
#         name = self.cleaned_data['name']
#         if len(name) < 3:
#             raise ValidationError('Название продукта должно содержать более 2 символов.')
#         return name
#
#     def clean_description(self):
#         description = self.cleaned_data['description']
#         X_WORDS = ['казино', 'некачественный']
#         for word in X_WORDS:
#             if word in description.lower():
#                 raise ValidationError(f'Описание не должен содержать {word}.')
#         return description
#
#     def clean_price(self):
#         price = self.cleaned_data['price']
#         if price < 0:
#             raise ValidationError('Цена продукта не может быть меньше 0.')
#         return price