from http.client import HTTPResponse
from unicodedata import category
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect

from django.views.generic import DetailView, ListView, DeleteView, UpdateView
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

# Create your views here.
def index(request):
    listings = ListingPost.objects.all().order_by('-id')
    listings_found = True
    avail_listings = []
    for listing in listings:
        if (listing.is_available == True):
            avail_listings.append(listing)
    if not avail_listings:
        listings_found = False

    return render(request, 'SwapProject/index.html',{'avail_listings':avail_listings, 'listings_found':listings_found})

# Logout
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('../')

# Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        account = authenticate(username=username, password=password)
        if account:
            if account.is_active:
                login(request, account)
                return HttpResponseRedirect('../')
        else:
            messages.error(request, 'Invalid username or password..')

    login_form = UserForm()
    return render(request, 'SwapProject/login.html', {'login_form':login_form})

# Register
def register(request):
    if request.method == 'POST':
        register_form = UserForm(data=request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.set_password(user.password)
            user.save()

            username = request.POST['username']
            password = request.POST['password']
            account = authenticate(username=username, password=password)

            if account:
                if account.is_active:
                    login(request, account)
                    return HttpResponseRedirect('../')
            return HttpResponseRedirect('../login')

        else:
            messages.error(request, 'Email or username is not valid.')

    register_form = UserForm() 
    return render(request, 'SwapProject/register.html', {'register_form':register_form})

# View Profile
class UserDetail(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'SwapProject/profile.html'

    def get_context_data(self, **kwargs):
        
        # Friends Feature
        friends = AppUser.objects.filter(user_id=self.kwargs.get('pk'))
        if len(friends) == 1:
            for user in friends:
                all_friends = user.friends.all()
                
        friend_requests = Friends.objects.all()
        current_app_user = AppUser.objects.get(user_id=self.kwargs.get('pk'))
        current_profile_user = AppUser.objects.get(user_id=self.request.user.id)
        friend_requesters = []
        
        friend_req_sent = False
        is_friend = False

        # Check if there's any friend request received
        for friend_request in friend_requests:
            if (friend_request.to_user_id == current_app_user.id) and (friend_request.from_user_id == current_profile_user.id):
                friend_req_sent = True
                break
    
        # Check for any friends
        for friend in all_friends:
            if friend.user_id == self.request.user.id: 
                is_friend = True
                break
        
        # Add all relevant friend requests in friend_requesters
        for friend_request in friend_requests:
            if friend_request.to_user_id == current_app_user.id:
                friend_requesters.append(AppUser.objects.get(id=friend_request.from_user_id))

        # Listing Feature
        listings = ListingPost.objects.all()
        user_posted = False
        for listing in listings:
            if (user.user_id == listing.user_id):
                user_posted = True
                break

        context = super().get_context_data(**kwargs)
        context['friend_req_sent'] = friend_req_sent
        context['is_friend'] = is_friend
        context['friends'] = all_friends
        context['friend_requesters'] = friend_requesters
        context['users'] = User.objects.all()
        context['listings'] = listings
        context['user_posted'] = user_posted
        context['current_app_user'] = current_app_user

        return context
    
# Update User Details    
class UserUpdate(UpdateView):
    model = User
    fields = ['first_name','username','email','password']
    success_url = '/'
    template_name = 'SwapProject/edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

# Create a Listing
def post_listing(request):
    if request.method == "POST":
        listing_form = ListingForm(request.POST, request.FILES)
        if listing_form.is_valid():
            listing = listing_form.save(commit=False)
            listing.user = request.user
            listing.is_available = True
            listing.save()
        return HttpResponseRedirect('../')

    listing_form = ListingForm()
    return render(request, 'SwapProject/upload.html',{'listing_form':listing_form})

# View Individual Listing
class ListingPostDetail(DetailView):
    model = ListingPost
    context_object_name = 'listing'
    template_name = 'SwapProject/listing.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listings = ListingPost.objects.all()
        context['listings'] = listings
        return context

# Delete a Listing
class ListingPostDelete(DeleteView):
    model = ListingPost
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listings'] = ListingPost.objects.all()
        return context

# Update Listing Details    
class ListingUpdate(UpdateView):
    model = ListingPost
    fields = ['title','description','image','category','size','condition','is_available']
    success_url = '/'
    template_name = 'SwapProject/edit_listing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listings'] = ListingPost.objects.all()
        context['listing'] = ListingPost.objects.get(user_id=self.request.user.id)
        return context

# Display Search Results
def search_listing(request):
    if request.method == 'GET':
        query = request.GET.get('listing')
        if len(query) > 0:
            search_results = ListingPost.objects.filter(title__icontains=query).distinct()
            listingposts = []
            for listingpost in search_results:
                listingposts.append(listingpost)
        return render(request, 'SwapProject/search.html', {'listings':listingposts, 'query':query})

# Search for Listings
class ListingList(ListView):
    model = ListingPost
    context_object_name = 'listings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listings'] = ListingPost.objects.all()
        return context
    
    def get_queryset(self):
        listing = get_object_or_404(ListingPost, title=self.kwargs.get('title'))
        return ListingPost.objects.filter(title=listing)

# Sending a Friend Request
def add_friend(request, current_user_id):
    # Get the user sending the friend request
    from_user = AppUser.objects.get(user_id=request.user)
    # Get the user receiving the friend request
    to_user = AppUser.objects.get(user_id=current_user_id)
    friend_request, created = Friends.objects.get_or_create(from_user=from_user, to_user=to_user)

    if created:
        messages.success(request, 'Friend request sent successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'Friend request failed to send..')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Accepting a Friend Request
def accept_friend(request, friend_request):
    app_user_id = AppUser.objects.get(user_id=request.user.id)
    #Check if user has multiple requests
    friend_requests = Friends.objects.filter(to_user_id=app_user_id.id)

    # Get the friend request objects
    friend_request = Friends.objects.get(to_user_id=app_user_id.id)
    from_app_user = AppUser.objects.get(id=friend_request.from_user_id)
    to_app_user = AppUser.objects.get(id=friend_request.to_user_id)
    if friend_request.to_user_id == app_user_id.id:
        to_app_user.friends_with.add(from_app_user)
        from_app_user.friends_with.add(to_app_user)
        # Delete friend request
        friend_request.delete()
        messages.success(request,'Friend request accepted.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request,'Friend request cannot be accepted.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Declining a friend request
def decline_friend(request, friend_request):
    app_user_id = AppUser.objects.get(user_id=request.user.id)
    friend_requests = Friends.objects.filter(to_user_id = app_user_id.id)
    for friend_req in friend_requests:
        print(friend_req.from_user_id)
        
    # Get the friend request object
    friend_request = Friends.objects.get(to_user_id=app_user_id.id)

    if friend_request.to_user_id == app_user_id.id:
        friend_request.delete()
        messages.success(request, 'Friend request declined..')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        messages.error(request, 'Friend request failed to decline..')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def forum(request):
    listings = ListingPost.objects.all().order_by('-id')
    categories = Category.objects.all()

    return render(request, 'SwapProject/forum.html',{'listings':listings, 'categories': categories}) 

class CategoryView(ListView):
    model = Category
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context

class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'SwapProject/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        categories = Category.objects.all()
        posts = Post.objects.all()

        context['posts'] = posts
        context['categories'] = categories
        return context

class PostListView(ListView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.all()
        return context

class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'SwapProject/post.html'
    
    def create_comment(self):
        comment_form = CommentForm(self.request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = self.user
            comment.post = self.post
            comment.save()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all()
        comments = Comment.objects.filter()
        post_comments = []
        for comment in comments:
            for post in posts:
                if (comment.post_id == post.id):
                    post_comments.append(comment)

        context['posts'] = posts
        context['comments'] = post_comments
        return context


def create_post(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect('../forum/')
        else:
            print(post_form.errors.as_data())
        

    post_form = PostForm()
    return render(request, 'SwapProject/create_post.html',{'post_form':post_form})

def chat(request):
    chat_rooms = ChatRoom.objects.all()

    # app_user_id = AppUser.objects.get(user_id=request.user.id)
    # current_chats = Chat.objects.filter(user_id=app_user_id.user_id)
    # current_chat_rooms = []
    # for chat in current_chats:
    #     current_chat_room = chat.room_id
    #     for room in chat_rooms:
    #         if (current_chat_room == room.id):
    #             print(room)
    #             if (room not in current_chat_rooms):
    #                 current_chat_rooms.append(room)



    return render(request, 'SwapProject/chat.html', {'current_chat_rooms':chat_rooms})

class Room(View):
    def get(self, request, room_name):
        room = ChatRoom.objects.filter(name = room_name).first()
        chats = []

        if room:
            chats = Chat.objects.filter(room = room)
        else:
            room = ChatRoom(name = room_name)
            room.save()
        return render(request, 'SwapProject/room.html', {'room_name':room_name, 'chats':chats}) 