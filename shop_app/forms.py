from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Product, Category


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательное поле. Введите действующий email.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

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