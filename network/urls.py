
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path('compose', views.compose, name="compose"),
    path('profile/<int:user_id>', views.profile, name="profile"),
    path('following', views.following, name="following"),
    path('follow', views.follow, name="follow"),
    path('unfollow', views.unfollow, name="unfollow")
]
