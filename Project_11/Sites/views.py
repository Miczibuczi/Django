from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import LoginForm, RegisterForm

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
            form.save()
            # add creating a fanpage for every new user
            # add creating a fanpage for every new user
            # add creating a fanpage for every new user
            # add creating a fanpage for every new user
            # add creating a fanpage for every new user
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "Sites/register.html", {"form":form})