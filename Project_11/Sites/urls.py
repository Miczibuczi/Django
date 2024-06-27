from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    path("register/", views.Register, name="register"),
    path("fanpage/<str:fanpage_name>/", views.Fanpage, name="fanpage"),
    path("wall/<str:username>/", views.UserWall_view, name="userwall"),
]