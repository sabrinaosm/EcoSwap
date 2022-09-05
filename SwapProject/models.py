from distutils.text_file import TextFile
from email.policy import default
from tkinter import CASCADE
from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField("AppUser", related_name='friends_with', blank=True)
    
    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            user_account = AppUser(user=instance)
            user_account.save()


class ListingPost(models.Model):
    user        = models.ForeignKey(User, related_name='listing', on_delete=models.DO_NOTHING)
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image       = models.ImageField(upload_to='static/SwapProject/')
    category    = models.CharField(max_length=50, blank=True)
    size        = models.CharField(max_length=50, blank=True)
    condition   = models.CharField(max_length=50, blank=True)
    posted_at   = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Friends(models.Model):
    from_user = models.ForeignKey(AppUser, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(AppUser, related_name='to_user', on_delete=models.CASCADE)

class Chat(models.Model):
    content = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)

class ChatRoom(models.Model):
    name = models.CharField(max_length=255)

class Category(models.Model):
    category_title = models.CharField(max_length=50)
    category_description = models.CharField(max_length=255)

    def __str__(self):
        return self.category_title

class Post(models.Model):
    user = models.ForeignKey(User, related_name="post_author", on_delete=models.DO_NOTHING)
    post_title = models.CharField(max_length=50)
    post_content = models.TextField(blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_title

class Comment(models.Model):
    user = models.ForeignKey(User, related_name="commenter", on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment