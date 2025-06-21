from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from app_carts.cart import move_cart
from .forms import SignUpForm, LoginForm
from .user import create_user


def signup_view(request):
    form = SignUpForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            password2 = form.cleaned_data.get('password2')
            if password == password2:
                user = create_user(username=username, email=email, password=password)
                if user:
                    login(request, user)
                    return redirect('home')
    return render(request, 'app_users/signup.html', {'form': form})


def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                current_session_key = request.session.session_key
                login(request, user)
                move_cart(request, current_session_key)
                return redirect('home')
    return render(request, 'app_users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
