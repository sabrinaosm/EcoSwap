from .models import *
from rest_framework import generics, mixins
from .serializer import *

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

class UserDetail(   mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    generics.GenericAPIView ):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class ListingPostList(generics.ListAPIView):
    queryset = ListingPost.objects.all()
    serializer_class = ListingPostListSerializer

class ListingPostDetail(    mixins.RetrieveModelMixin, 
                            mixins.UpdateModelMixin, 
                            mixins.DestroyModelMixin, 
                            generics.GenericAPIView):
    queryset = ListingPost.objects.all()
    serializer_class = ListingPostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryViewSerializer

class CategoryDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

class PostDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)