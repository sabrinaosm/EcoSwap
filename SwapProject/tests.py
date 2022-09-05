import json
from urllib import response

from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

# Testing asynchronous channels
from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from .model_factories import *
from .serializer import *


# Test: Retrieving User Details
class UserTest(APITestCase):
    def test_getUserDetailSuccess(self):
        user = UserFactory.create(pk=1, username='test', first_name='Test', email='test@mail.com')
        url = reverse('user_api', kwargs={'pk':1})
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)

    def test_getUserDetailError(self):
        url = '/api/profile/Test2'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

# Test: Updating User Details
class UserPutTest(TestCase):
    def test_updateUserSuccess(self):
        user = User.objects.create(username='TestUpdateUser')
        response = self.client.post(reverse('edit_profile', kwargs={'pk': user.id}), {'username':'TestUpdateSuccess', 
        'first_name':'SuccessUpdate', 
        'email':'successupdate@mail.com', 
        'password':'successpassword', 
        'groups':'', 
        'user_permissions':'', 
        'is_staff':False, 
        'is_active':True, 
        'is_superuser':False, 
        'last_login':'2022-08-24', 
        'date_joined':'2022-08-22'})
        self.assertEqual(response.status_code, 302)

    def test_updateUserError(self):
        url = '/api/profile/Test4'
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

# Test: Listing Post
class ListingPostTest(TestCase):
    # Success Test: Retrieving Listing Post
    def test_getListingPostSuccess(self):
        listing = ListingPostFactory.create(pk=5)
        url = reverse('listing_api', kwargs={'pk':5})
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200) 
    
    # Failure Test: Retrieving Listing Post
    def test_getListingPostError(self):
        listing = ListingPostFactory.create(pk=6, id='listingtest6')
        url = '/api/post/listingtest6/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    # Success Test: Deleting Listing Post
    def test_deleteListingPostSuccess(self):
        listing = ListingPostFactory.create(pk=7)
        url = reverse('listing_api', kwargs={'pk':7})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
    
    # Failure Test: Deleting Listing Post
    def test_deleteListingPostError(self):
        listing = ListingPostFactory.create(pk=8, id='listingtest8')
        url = '/api/post/listingtest8'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    # Success Test: Updating Listing Post
    def test_updateListingPostSuccess(self):
        user = UserFactory.create(pk=11, username='test11', first_name='Test11', email='test11@mail.com')
        listing = ListingPost.objects.create(user=user, 
        title='Testing Title', 
        description='Testing Description', 
        image='/static/SwapProject/testImage', 
        category='Test Category', 
        size='Test Size', 
        condition='Test Condtion', 
        posted_at = '2022-09-01T04:43:14.193027Z')
        response = self.client.post(reverse('edit_listing', kwargs={'pk': listing.id}), {'user':user, 
        'title':'Testing Title Update Success', 
        'description':'Testing Description Update Success', 
        'image':'/static/SwapProject/testimage11.jpg', 
        'category':'Test Category', 
        'size':'Test Size', 
        'condition':'Test Condtion', 
        'posted_at':'2022-09-02T04:43:14.193027Z'})
        self.assertEqual(response.status_code, 302)

    # Failure Test: Updating Listing Post
    def test_updateListingPostError(self):
        url = '/api/listing/Test12'
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)