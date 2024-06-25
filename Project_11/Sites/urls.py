from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.Login, name="login"),
    path("register/", views.Register, name="register"),
    path("fanpage/", views.Fanpage, name="fanpage"),
]