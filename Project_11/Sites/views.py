from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from .models import UserWall
from django.contrib.auth.models import User

def index(request):
    if request.user.is_authenticated:
        return redirect("fanpage")
    else:
        return redirect("login")


def Login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            messages.info(request, f"Welcome {username}")
            return render(request, "base.html", {"user":user})
        else:
            messages.error(request, "Invalid username or password")
    form = LoginForm
    return render(request, "Sites/login.html", {"form":form})

def Fanpage(request):
    return render(request, "Sites/fanpage.html, {}")

def Register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            user = User.objects.create_user(username=username, email=email)
            user.set_password(form.cleaned_data["password"])
            user.save()
            UserWall.objects.create(user=user)
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "Sites/register.html", {"form":form})    