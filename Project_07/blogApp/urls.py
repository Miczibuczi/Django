from . import views
from django.urls import path, include

urlpatterns = [
    path("", views.postslist.as_view(), name="home"),
    path("post-detail/<slug:slug>", views.postdetail.as_view(), name="post_detail"),
]