from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path('', views.home, name="home"),
    path('post/<str:pk>/', views.blog_post, name="post"),
    path("create_post/", views.create_post, name="create-post"),
    path("update_post/<str:pk>/", views.update_post, name="update-post"),
    path("delete-post/<str:pk>/", views.delete_post, name="delete-post"),
    path("register/", views.register_user, name="register"),
    path("delete-comment/<str:pk>/", views.delete_comment, name="delete-comment"),
    path("profile/<str:pk>/", views.profile, name="profile"),
    path("profile-update/", views.update_profile, name="profile-update"),
    path('about/', views.about, name="about"),
               ]
