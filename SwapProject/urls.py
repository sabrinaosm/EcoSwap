from . import views
from . import api
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Home Page
    path('', views.index, name='index'),
    # Login
    path('login/', views.user_login, name='name'),
    # Register
    path('register/', views.register, name='register'),
    # Logout
    path('logout/', views.user_logout, name='logout'),
    # Account
    path('profile/<int:pk>', views.UserDetail.as_view(), name='profile'),
    # Update User Details
    path('update/<int:pk>', login_required(login_url='../login/')(views.UserUpdate.as_view()), name='edit_profile'),
    # Post Listing
    path('upload/', views.post_listing, name='create_listing'),
    # View Listing
    path('listing/<int:pk>', views.ListingPostDetail.as_view(), name='listing'),
    # Delete Listing
    path('delete_listing/<int:pk>', views.ListingPostDelete.as_view(), name='listing_delete'),
    # Search for Listing
    path('search/', views.search_listing, name='search_listing'),
    # Send friend request
    path('add_friend/<int:current_user_id>', views.add_friend, name='add_friend'),
    # Accept friend request
    path('accept_friend/<int:friend_request>', views.accept_friend, name='accept_friend'),
    # Declining friend request
    path('decline_friend/<int:friend_request>', views.decline_friend, name='decline_friend'),
    
    # Forum
    path('forum/', views.forum, name='forum'),
    # Category of Forum
    path('category/<int:pk>', views.CategoryDetailView.as_view(), name="category"),
    # Create a Post
    path('create_post/', views.create_post, name='create_post'),
    # Individual Post of Forum
    path('post/<int:pk>', views.PostDetail.as_view(), name='post'),
    
    # Chat
    path('chat/', views.chat, name='chat'),
    # Chat Room 
    path('chat/<str:room_name>/', views.Room.as_view(), name='room'),
    # Update Listing Details
    path('update/<int:pk>/', views.ListingUpdate.as_view(), name='edit_listing'),

    #API
    path('api/users', api.UserList.as_view(), name='users_api'),
    path('api/profile/<int:pk>', api.UserDetail.as_view(), name='user_api'),
    path('api/listings', api.ListingPostList.as_view(), name='listings_api'),
    path('api/listing/<int:pk>', api.ListingPostDetail.as_view(), name='listing_api'),
    path('api/categories', api.CategoryView.as_view(), name='categories_api'),
    path('api/category/<int:pk>', api.CategoryDetailView.as_view(), name='category_api'),
    path('api/posts', api.PostListView.as_view(), name='posts_api'),
    path('api/post/<int:pk>', api.PostDetail.as_view(), name='post_api')
]