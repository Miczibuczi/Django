from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm, PostForm
from .models import UserWall
from django.contrib.auth.models import User
from django.urls import reverse

def Index(request):
    if request.user.is_authenticated:
        username = request.user.username
        return redirect(reverse("userwall", kwargs={'username': username}))
    else:
        return redirect("login")


def Login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f"Welcome {username}")
            return redirect(reverse("userwall", kwargs={'username': username}))
        else:
            messages.error(request, "Invalid username or password")
    form = LoginForm
    return render(request, "Sites/login.html", {"form":form})

def Logout(request):
    logout(request)
    return redirect("login")

def Fanpage(request):
    if request.user.is_authenticated:
        user = request.user
        posts = user.wall.posts.all()
        return render(request, "Sites/fanpage.html", {"user":user, "posts":posts})
    else:
        return redirect("login")

def UserWall_view(request, username):
    user = get_object_or_404(User, username=username)
    if user.is_authenticated:
        posts = user.wall.posts.all().order_by("-created_at")
        return render(request, "Sites/fanpage.html", {"user":user, "posts":posts})
    else:
        return redirect("login")

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

def Create_wall_post(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.wall = user.wall
            post.save()
            return redirect("userwall", username=username)
    else:
        form = PostForm()
    return render(request, "Sites/post.html", {"form":form})

def Create_fanpage_post(request, fanpage_name):
    pass