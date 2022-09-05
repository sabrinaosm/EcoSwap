import factory
from django.test import TestCase
from django.conf import settings
from django.core.files import File

from .models import *

class AppUserFactory(factory.django.DjangoModelFactory):
    user_id = '10'

    class Meta:
        model = AppUser

class UserFactory(factory.django.DjangoModelFactory):
    first_name = 'NameTest'
    username = 'UsernameTest'
    email = 'test@mail.com'

    class Meta:
        model = User

class ListingPostFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    title = 'Test Title Post'
    description = 'Description Title Post'
    image = 'static/SwapProject/test.jpg'
    category = 'Tops'
    size = 'Small'
    condition = 'Brand New'
    posted_at = '2022-08-24 16:14:22.20676+08' 

    class Meta:
        model = ListingPost