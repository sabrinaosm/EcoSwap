from unicodedata import category
from rest_framework import serializers
from .models import *

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'username', 'email'] 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.first_name = validated_data.get('first_name', instance.first_name)

class ListingPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingPost
        fields = ['user','title','description','image','category','size','condition','posted_at']

class ListingPostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ListingPost
        fields = ['user','title','description','image','category','size','condition','posted_at']
    
    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.size = validated_data.get('size', instance.size)
        instance.condition = validated_data.get('condition', instance.condition)

class CategoryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_title', 'category_description']

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_title', 'category_description']

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user','post_title', 'post_content', 'posted_at','category']

class PostDetailSerializer(serializers.ModelSerializer):
    user = UserListSerializer()
    category = CategoryViewSerializer()

    class Meta:
        model = Post
        fields = ['user','post_title', 'post_content', 'posted_at','category']