from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from users.forms import CustomSignUpForm, CustomLogInForm

@login_required(login_url='login')
def home(request):
    user = 'User'
    if request.user.is_authenticated:
        user = request.user.username
    return render(request, 'users/home.html', {'username': user})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error signing up. Please check your details.')
    else:
        form = CustomSignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = CustomLogInForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('home')
        messages.error(request, 'Invalid email or password')
    else:
        form = CustomLogInForm()
    return render(request, 'users/login.html', {'form': form})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')
