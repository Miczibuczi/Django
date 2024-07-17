from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm, PostForm, FanpageForm
from .models import UserWall, Fanpage, LastVisited, Friendship
from django.contrib.auth.models import User
from django.urls import reverse

# utility function
def get_visited_with_counts(user):
    last_visited, _ = LastVisited.objects.get_or_create(user=user)
    visited_with_counts = []
    for url in last_visited.last_visited:
        if url.startswith("wall/"):
            username = url.split("/")[1]
            wall = get_object_or_404(UserWall, user__username=username)
            visited_with_counts.append({"url":url, "views":wall.views})
        elif url.startswith("fanpage/"):
            fanpage_name = url.split("/")[1]
            fanpage = get_object_or_404(Fanpage, fanpage_name=fanpage_name)
            visited_with_counts.append({"url":url, "views":fanpage.views})
    
    return visited_with_counts


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
    form = LoginForm
    return render(request, "Sites/login.html", {"form":form})

def Logout(request):
    logout(request)
    return redirect("login")

def Fanpage_view(request, fanpage_name):
    user = request.user
    fanpage = get_object_or_404(Fanpage, fanpage_name=fanpage_name)
    if user.is_authenticated:
        fanpage.views += 1
        fanpage.save()
        last_visited, _ = LastVisited.objects.get_or_create(user=user)
        last_visited.update_last_visited(f"fanpage/{fanpage.fanpage_name}/")
        visited_with_counts = get_visited_with_counts(request.user)
        posts = fanpage.posts.all().order_by("-created_at")
        return render(request, "Sites/fanpage.html", {"user":user, "posts":posts, "fanpage":fanpage, "last_visited":visited_with_counts})
    else:
        return redirect("login")

def UserWall_view(request, username):
    user = get_object_or_404(User, username=username)
    if user.is_authenticated:
        user.wall.views += 1
        user.wall.save()
        last_visited, _ = LastVisited.objects.get_or_create(user=request.user)
        last_visited.update_last_visited(f"wall/{user.username}/")
        visited_with_counts = get_visited_with_counts(request.user)
        posts = user.wall.posts.all().order_by("-created_at")
        friends = Friendship.get_friends(user)
        sent_invitations = Friendship.get_sent_invitations(user)
        received_invitations = Friendship.get_received_invitations(user)
        return render(request, "Sites/userwall.html", {"user":user, "posts":posts, "last_visited":visited_with_counts, "request":request, "friends":friends, "sent_invitations":sent_invitations, "received_invitations":received_invitations})
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
        visited_with_counts = get_visited_with_counts(request.user)
    return render(request, "Sites/post.html", {"form":form, "last_visited":visited_with_counts})

def Create_fanpage_post(request, fanpage_name):
    user = request.user
    fanpage = get_object_or_404(Fanpage, fanpage_name=fanpage_name)
    if request.method == "POST" and user == fanpage.user:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.fanpage = fanpage
            post.save()
            return redirect("fanpage", fanpage_name=fanpage.fanpage_name)
    elif user != fanpage.user:
        messages.error(request, "You can make posts only on your fanpages")
        return redirect("user_details")
    else:
        form = PostForm()
        visited_with_counts = get_visited_with_counts(request.user)
    return render(request, "Sites/post.html", {"form":form, "last_visited":visited_with_counts})

def Create_fanpage_view(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = FanpageForm(request.POST)
            if form.is_valid():
                fanpage = form.save(commit=False)
                fanpage.user = request.user
                fanpage.save()
                return redirect("fanpage", fanpage_name=fanpage.fanpage_name)
        else:
            return redirect("login")
    else:
        form = FanpageForm()
        visited_with_counts = get_visited_with_counts(request.user)
    return render(request, "Sites/create_fanpage.html", {"form":form, "last_visited":visited_with_counts})

def User_details(request):
    user = get_object_or_404(User, username=request.user.username)
    fanpages = user.fanpage.all()
    visited_with_counts = get_visited_with_counts(request.user)
    return render(request, "Sites/user_details.html", {"user":user, "fanpages":fanpages, "last_visited":visited_with_counts})

def Search(request):
    query = request.GET.get("query")
    fanpages = Fanpage.objects.filter(fanpage_name__icontains=query)
    walls = UserWall.objects.filter(user__username__icontains=query)
    visited_with_counts = get_visited_with_counts(request.user)
    if len(fanpages) + len(walls) == 1:
        if len(fanpages) == 1:
            return redirect("fanpage", fanpage_name=fanpages[0].fanpage_name)
        else:
            return redirect("userwall", username=walls[0].user.username)
    else:
        return render(request, "Sites/search_results.html", {"fanpages":fanpages, "walls":walls, "query":query, "last_visited":visited_with_counts})
    
def Send_friend_request(request, username):
    receiver = get_object_or_404(User, username=username)
    friendship, created = Friendship.objects.get_or_create(sender=request.user, receiver=receiver)
    if created:
        friendship.save()
        messages.info(request, f"Invitation sent to {receiver.username}")
    elif friendship.status == "accepted":
        messages.error(request, f"{receiver.username} already is your friend")
    elif friendship.status == "pending":
        messages.error(request, "Invitation already sent")
    else:
        messages.error(request, "Unknown error. Check the Send_friend_request view")
    return redirect("friends_details", username=request.user)

def Accept_friend_request(request, username):
    sender = get_object_or_404(User, username=username)
    friendship = get_object_or_404(Friendship, sender=sender, receiver=request.user)
    if friendship.status == "accepted":
        messages.error(request, f"You've already accepted the invitation from {sender}")
    else:
        friendship.status = "accepted"
        friendship.save()
        messages.info(request, "Friend request accepted")
    return redirect("friends_details", username=request.user)

def Friends_details(request, username):
    return render(request, "Sites/friends_details.html")