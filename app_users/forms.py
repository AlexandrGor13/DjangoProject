from django import forms
from django.contrib.auth.forms import AuthenticationForm


class SignUpForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=12, label='Имя пользователя', help_text='Обязательное поле. Введите имя пользователя.')
    email = forms.EmailField(min_length=5, max_length=20, label='Электронная почта', help_text='Обязательное поле. Введите действующий email.')
    password = forms.CharField(min_length=8, max_length=20, widget=forms.PasswordInput, label='Пароль', help_text='Обязательное поле. Введите пароль (не менее 8 символов).')
    password2 = forms.CharField(min_length=8, max_length=20, widget=forms.PasswordInput, label='Подтверждение пароля', help_text='Обязательное поле. Введите пароль (не менее 8 символов).')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
