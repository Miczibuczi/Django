from django.shortcuts import render
from .models import posts
from django.views import generic
from django.views.decorators.http import require_GET
from django.http import HttpResponse

class postslist(generic.ListView):
    queryset = posts.objects.filter(status=1).order_by("-created_on")
    template_name = "blogApp/home.html"
    paginate_by = 4

class postdetail(generic.DetailView):
    model = posts
    template_name = "blogApp/post.html"