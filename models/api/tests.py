from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from models import Apartment
from models import *
from django.core import management
from api import urls
from api import views
import unittest
import json
from django.contrib.auth.hashers import *
import os
import hmac
from django.conf import settings


#Tests for Models Layer

#Test for Create API
class CreateTestCase(TestCase):
        # management.call_command('loaddata', 'db.json', verbosity=0)
        def setUp(self):
            self.user = User.objects.create(username = "hungryeung", password = make_password("password"), email = "cy4bv@virginia.edu")
            authenticator_value = hmac.new(
                key=settings.SECRET_KEY.encode('utf-8'),
                msg=os.urandom(32),
                digestmod='sha256',
            ).hexdigest()
            self.auth = Authenticator.objects.create(user_id = self.user.id,authenticator=authenticator_value)

        def test_apartment_name_valid(self):
            data = {
                "name": "Apartment 8",
                "price": 999,
                "auth":self.auth.authenticator
            }
            response = self.client.post('/api/v1/create/',data)
            self.assertEqual(response.status_code,200)
        #not a valid post request
        def test_apartment_name_invalid(self):
            response = self.client.get('/api/v1/create/').json()
            self.assertEqual(response['valid'], False)

#Testing the Delete API
class DeleteTestCase(TestCase):
    # management.call_command('loaddata', 'db.json', verbosity=0)
    def setUp(self):
        self.user = User.objects.create(username="hungryeung", password=make_password("password"),
                                        email="cy4bv@virginia.edu")
        authenticator_value = hmac.new(
            key=settings.SECRET_KEY.encode('utf-8'),
            msg=os.urandom(32),
            digestmod='sha256',
        ).hexdigest()
        self.auth = Authenticator.objects.create(user_id=self.user.id, authenticator=authenticator_value)

        apt_data = {
            "name": "Apartment 9",
            "price": 999,
            "auth": self.auth.authenticator
        }
        response1 = self.client.post('/api/v1/create/', apt_data).json()

    def test_delete_apartment(self):
        response = self.client.get(reverse('delete', kwargs={'id': 2})).json()
        self.assertEqual(response['valid'], True)
    def test_delete_apartment_invalid(self):
        response = self.client.post(reverse('delete', kwargs={'id': 2})).json()
        self.assertEqual(response['valid'], False)
    def test_delete_apartment_invalid_id(self):
        response = self.client.get(reverse('delete', kwargs={'id': 2})).json()
        self.assertEqual(response['message'],  'Apartment does not exist.')


#Testing the Update API

class UpdateTestCase(TestCase):
    # management.call_command('loaddata', 'db.json', verbosity=0)
    def setUp(self):
        self.user = User.objects.create(username="hungryeung", password=make_password("password"),
                                        email="cy4bv@virginia.edu")
        authenticator_value = hmac.new(
            key=settings.SECRET_KEY.encode('utf-8'),
            msg=os.urandom(32),
            digestmod='sha256',
        ).hexdigest()
        self.auth = Authenticator.objects.create(user_id=self.user.id, authenticator=authenticator_value)

        apt_data = {
            "name": "Apartment 10",
            "price": 999,
            "auth": self.auth.authenticator
        }
        response1 = self.client.post('/api/v1/create/', apt_data).json()

    def test_update_apartment(self):
        update_data = {
            "name": "Apartment Updated Name",
            "price": 1750,
        }
        response = self.client.post(reverse('update', kwargs={'id': 3}),update_data).json()
        self.assertEqual(response['message'], 'Updated the Apartment.')

    def test_update_apartment_invalid(self):
        response = self.client.get(reverse('update', kwargs={'id': 3})).json()
        self.assertEqual(response['valid'], False)

#Testing authentication getter view
class AuthTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="hungryeung", password=make_password("password"),
                                        email="cy4bv@virginia.edu")
        authenticator_value = hmac.new(
            key=settings.SECRET_KEY.encode('utf-8'),
            msg=os.urandom(32),
            digestmod='sha256',
        ).hexdigest()
        self.auth = Authenticator.objects.create(user_id=self.user.id, authenticator=authenticator_value)

    def test_auth(self):
        auth_update_data = {
            "auth": self.auth.authenticator
        }
        response = self.client.post(reverse('auth'), auth_update_data).json()
        self.assertEqual(response['message'], 'Authenticator exists')

    def test_auth_invalid(self):
        auth_update_data = {
            "auth": 1
        }
        response = self.client.post(reverse('auth'), auth_update_data).json()
        self.assertEqual(response['valid'], False)

#Tests logout API which should remove the authenticator during logout process (if it exists)
class LogoutTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="hungryeung", password=make_password("password"),
                                        email="cy4bv@virginia.edu")
        authenticator_value = hmac.new(
            key=settings.SECRET_KEY.encode('utf-8'),
            msg=os.urandom(32),
            digestmod='sha256',
        ).hexdigest()
        self.auth = Authenticator.objects.create(user_id=self.user.id, authenticator=authenticator_value)

    def test_logout(self):
        auth_data = {
            "auth": self.auth.authenticator
        }
        response = self.client.post(reverse('logout'), auth_data).json()
        self.assertEqual(response['message'], 'Authenticator removed successfully')

    #authenticator does not exist should give back an error
    def test_logout_invalid(self):
        auth_update_data = {
            "auth": 1
        }
        response = self.client.post(reverse('auth'), auth_update_data).json()
        self.assertEqual(response['message'],'Authenticator does not exist.')

#Tests Login API which should remove the authenticator during logout process (if it exists)
class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="hungryeung", password=make_password("password"),
                                        email="cy4bv@virginia.edu")
        authenticator_value = hmac.new(
            key=settings.SECRET_KEY.encode('utf-8'),
            msg=os.urandom(32),
            digestmod='sha256',
        ).hexdigest()
        self.auth = Authenticator.objects.create(user_id=self.user.id, authenticator=authenticator_value)
        self.user.save()
        self.auth.save()

    def test_login(self):
        login_data = {
            "username":"hungryeung",
            "password": "password"
        }
        response = self.client.post(reverse('login'), login_data).json()
        self.assertEqual(response['message'],  'User is already authenticated.')

    def test_login_invalid_username(self):
        login_data = {
            "username":"baduser",
            "password": "password"
        }
        response = self.client.post(reverse('login'), login_data).json()
        self.assertEqual(response['message'],'Username does not exist.')

    def test_login_invalid_password(self):
        login_data = {
            "username": "hungryeung",
            "password": "badpassword"
        }
        response = self.client.post(reverse('login'), login_data).json()
        self.assertEqual(response['message'], 'Password incorrect.')

    def test_login_invalid_request(self):
        response = self.client.get(reverse('login')).json()
        self.assertEqual(response['message'],'Not a POST request.')

#Tests all cases of the signup API
class SignupTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="hungryeung", password=make_password("password"),
                                        email="cy4bv@virginia.edu")
        authenticator_value = hmac.new(
            key=settings.SECRET_KEY.encode('utf-8'),
            msg=os.urandom(32),
            digestmod='sha256',
        ).hexdigest()
        self.auth = Authenticator.objects.create(user_id=self.user.id, authenticator=authenticator_value)
        self.user.save()
        self.auth.save()
    def test_signup(self):
        login_data = {
            "username": "cyeung",
            "password":"password",
            "email":"someemail@virginia.edu"
        }
        response = self.client.post(reverse('signup'), login_data).json()
        self.assertEqual(response['message'], 'Created new User.')
    def test_signup_invalid(self):
        response = self.client.get(reverse('signup')).json()
        self.assertEqual(response['message'], 'Not a POST request.')
    def test_signup_invalid_username(self):
        login_data = {
            "username": "hungryeung",
            "password": "password",
            "email": "email@virginia.edu"
        }
        response = self.client.post(reverse('signup'), login_data).json()
        self.assertEqual(response['message'], 'Username already exists.')
    def test_signup_invalid_email(self):
        login_data = {
            "username": "cyeung",
            "password": "password",
            "email": "cy4bv@virginia.edu"
        }
        response = self.client.post(reverse('signup'), login_data).json()
        self.assertEqual(response['message'], "Email already has an associated account.")

#Tests getting item api
class ItemTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="hungryeung", password=make_password("password"),
                                        email="cy4bv@virginia.edu")
        authenticator_value = hmac.new(
            key=settings.SECRET_KEY.encode('utf-8'),
            msg=os.urandom(32),
            digestmod='sha256',
        ).hexdigest()
        self.auth = Authenticator.objects.create(user_id=self.user.id, authenticator=authenticator_value)
        self.user.save()
        self.auth.save()
        data = {
            "name": "Chris Apartment",
            "price": 999,
            "auth": self.auth.authenticator
        }
        response = self.client.post('/api/v1/create/', data)
    #should get the apartment (valid)
    def test_item(self):
        response = self.client.get(reverse('item', kwargs={'id': 5})).json()
        self.assertEqual(response['valid'],True)
    #should not get the apartment (invalid id)
    def test_item_invalid(self):
        response = self.client.get(reverse('item', kwargs={'id': 300})).json()
        self.assertEqual(response['message'],'Apartment does not exist.')

#Tests the price_list api which gets the five cheapest apartments
class getPriceListTestCase(TestCase):
    def setup(self):
        self.user = User.objects.create(username="hungryeung", password=make_password("password"),
                                        email="cy4bv@virginia.edu")
        authenticator_value = hmac.new(
            key=settings.SECRET_KEY.encode('utf-8'),
            msg=os.urandom(32),
            digestmod='sha256',
        ).hexdigest()
        self.auth = Authenticator.objects.create(user_id=self.user.id, authenticator=authenticator_value)
        self.user.save()
        self.auth.save()
        # Apartment.objects.create(name="a", price=10, rating=0.5, auth=self.auth.authenticator)
        # Apartment.objects.create(name="b", price=20, rating=1.5,auth=self.auth.authenticator)
        # Apartment.objects.create(name="c", price=30, rating=2.5,auth=self.auth.authenticator)
        # Apartment.objects.create(name="d", price=40, rating=3.5,auth=self.auth.authenticator)
        # Apartment.objects.create(name="e", price=50, rating=4.5,auth=self.auth.authenticator)
        # Apartment.objects.create(name="f", price=60, rating=4.8,auth=self.auth.authenticator)
    def test_PriceList(self):
        response = self.client.get('/api/v1/price_list/')
        self.assertEqual(response.status_code, 200)
    # def test_PriceList_accurate(self):
    #     apt_a = Apartment.objects.get(name="a")
    #     apt_a.save()
    #     apt_b = Apartment.objects.get(name="b")
    #     apt_b.save()
    #     apt_c = Apartment.objects.get(name="c")
    #     apt_c.save()
    #     apt_d = Apartment.objects.get(name="d")
    #     apt_d.save()
    #     apt_e = Apartment.objects.get(name="e")
    #     apt_e.save()
    #     apt_f = Apartment.objects.get(name="f")
    #     apt_f.save()
    #     objects = list(Apartment.objects.all().order_by('price')[:5])
    #     response = self.client.get('/api/v1/price_list/').json()
    #     name_list = []
    #     for apartment in response['result']:
    #         name_list.append(apartment.name)
    #     print(name_list)
    #     self.assertEqual(name_list, ['a', 'b', 'c', 'd', 'e'])

#Testing getting the top list (top 5 apartments by rating) api
class getTopListTestCase(TestCase):
    def test_Toplist(self):
        response = self.client.get('/api/v1/top_list/').json()
        self.assertEqual(response['valid'], True)

#Testing getting the entire (all) apartments list
class getListTestCase(TestCase):
    def test_Toplist(self):
        response = self.client.get('/api/v1/list/').json()
        self.assertEqual(response['valid'], True)



