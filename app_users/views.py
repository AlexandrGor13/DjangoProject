from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout

from app_cart.cart import move_cart
from .forms import SignUpForm, LoginForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
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
