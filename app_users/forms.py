from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(max_length=254, help_text='Обязательное поле. Введите действующий email.')
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=12, label='Имя пользователя')
    email = forms.EmailField(label='Электронная почта')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Подтверждение пароля')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
