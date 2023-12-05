from django.urls import path, include
from . import views

urlpatterns = [
    path("<int:id>", views.post_detailview, name="post_detail"),
    path("", views.index, name="index")
]