from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index, name="index"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    path("register/", views.Register, name="register"),
    path("wall/<str:username>/", views.UserWall_view, name="userwall"),
    path("wall/<str:username>/post/", views.Create_wall_post, name="create_wall_post"),
    path("fanpage/create/", views.Create_fanpage_view, name="create_fanpage"),
    path("fanpage/<str:fanpage_name>/", views.Fanpage_view, name="fanpage"),
    path("fanpage/<str:fanpage_name>/post/", views.Create_fanpage_post, name="create_fanpage_post"),
    path("user_details/", views.User_details, name="user_details"),
    path("serach/", views.Search, name="search"),
    path("add_friend/<str:username>/", views.Send_friend_request, name="send_invitation"),
    path("accept_friend/<str:username>/", views.Accept_friend_request, name="accept_invitation"),
    path("friends_details/", views.Friends_details, name="friends_details"),
    path("reject_friend/<str:username>/", views.Reject_friend_request, name="reject_invitation"),
    path("delete_friendship/<str:username>", views.Delete_friendship, name="delete_friendship"),
    path("cancel_invitation/<str:username>", views.Cancel_friend_request, name="cancel_invitation")
]