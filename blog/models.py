from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from cloudinary.models import CloudinaryField

# Create your models here.
class User(AbstractUser):
    profile_pic = models.ImageField(upload_to="avatar/", default='avatar.svg')
    # profile_pic = CloudinaryField('image')
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    title = models.CharField(max_length=200)
    topics = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    post_image = models.ImageField(upload_to="images/", blank=True)
    # post_image = CloudinaryField('image')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    # no_of_likes = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created", "-updated"]


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ["-created"]
