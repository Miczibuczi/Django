from django.shortcuts import render, redirect
from .forms import CommentForm
from .models import Comment, Post
from django.urls import reverse

def post_detailview(request, id):
    post = Post.objects.get(id=id)
    comments = post.comments.all()
    if request.method == "POST":
        cf = CommentForm(request.POST or None)
        if cf.is_valid():
            content = request.POST.get("content")
            comment = Comment.objects.create(post = post, user = request.user, content = content)
            comment.save()
            return redirect(reverse("post_detail", args=[str(post.id)]))
    else:
        cf = CommentForm()
        
        context ={
            "comment_form":cf,
            "post":post,
            "comments":comments,
        }
        return render(request, "CommentsApp/post_detail.html", context)
    
def index(request):
    posts = Post.objects.all()
    return render(request, "CommentsApp/index.html", {"posts": posts})