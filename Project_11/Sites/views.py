from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import LoginForm

def index(request):
    return render(request, "base.html", {})


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