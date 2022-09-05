from .models import *
from django import forms
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model   = User
        fields  = ('first_name', 'username', 'email', 'password')

class ListingForm(forms.ModelForm):
    class Meta:
        model   = ListingPost
        fields  = ('title', 'description', 'image', 'category', 'size', 'condition','is_available',)
        labels = {'title':'', 'description':'', 'image':'', 'category':'', 'size':'', 'condition':'', 'is_available':''}

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_title','post_content',)
        labels = {'post_title':'','post_content':'',}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        