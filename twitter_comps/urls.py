from django.urls import path
from .views import *


app_name = "twitter_comps"

urlpatterns = [

    path('', landing, name="landing"),
    
    path('home/', home, name="home"),
    path("registration/", registration_page, name="registration_page"),
    path("login/", login_page, name="login_page"),

    path("logout/", logout_page, name="logout"),
    path("profile_view/<int:id>/", profile_view, name="profile_view"),
    path("edit-profile/<int:id>/", edit_profile, name="edit_profile"),

    path("delete-post/<int:id>/", delete_post, name="delete_post"),
    path("like-post/<int:id>/", like_post, name="like_post"),
    path("like-view/<int:id>/", view_likes, name="view_likes"),

    path("comment_post/<int:id>/", comment_post, name="comment_post"),
    path("delete_comment/<int:id>/", delete_comment, name="delete_comment"),
    path("retweet/<int:id>/", retweet, name="retweet"),
    
    path("profiles/", view_users, name="profiles"),
    path("follow/<int:id>/", add_follower, name="add_follower"),
]

