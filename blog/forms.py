from django.forms import ModelForm
from .models import Post, User
from django.contrib.auth.forms import UserCreationForm


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        # exclude = ["author"]


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "username", "password1","password2"]

    
class UpdateUser(ModelForm):
    class Meta:
        model = User
        fields = [ "profile_pic", "email", "username", "bio"]
