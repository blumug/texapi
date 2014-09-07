import json

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.core.urlresolvers import reverse

from rest_framework.authtoken.models import Token

from models import ApiUser


class TestApi(TestCase):

    def setUp(self):
        pass

    def test_login_wrong_data(self):
        c = Client()

        data = {
            'email': 'test@test.com',
            'password': 'foo',
        }
        json_data = json.dumps(data)
        res = c.post(reverse('api_login'), json_data, content_type='application/json')
        self.assertEquals(res.status_code, 401)

    def test_create_token(self):
        user = User.objects.create(username='user')
        ApiUser.objects.create(user=user)

        self.assertEquals(Token.objects.all().count(), 1)

        token = Token.objects.all()[0]
        self.assertEquals(token.user.id, user.id)

    def test_login_ok(self):
        user = User.objects.create(username='user', email='test@test.com', is_active=True)
        ApiUser.objects.create(user=user)
        user.set_password('password')
        user.save()

        c = Client()

        data = {
            'email': 'test@test.com',
            'password': 'password',
        }
        json_data = json.dumps(data)
        res = c.post(reverse('api_login'), json_data, content_type='application/json')
        self.assertEquals(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEquals(data.get('token'), Token.objects.get(user=user).key)

    def test_login_twitter_ko(self):
        user = User.objects.create(username='user', email='test@test.com', is_active=True)
        ApiUser.objects.create(user=user)
        user.set_password('password')
        user.save()

        c = Client()

        data = {
            'twitter_token': 'foo',
            'twitter_token_secret': 'bar',
            'twitter_screen_name': 'screename',
            'twitter_id': 'twitter_id',
        }
        json_data = json.dumps(data)
        res = c.post(reverse('api_login'), json_data, content_type='application/json')
        self.assertEquals(res.status_code, 401)

    def test_signup(self):
        c = Client()
        data = {'email': 'test@test.com', 'password': 'password'}
        json_data = json.dumps(data)
        res = c.post(reverse('api_signup'), json_data, content_type='application/json')
        self.assertEquals(res.status_code, 200)
        data = json.loads(res.content)
        user = User.objects.get(pk=1)
        self.assertEquals(user.email, 'test@test.com')
        self.assertEquals(data.get('token'), Token.objects.get(user=user).key)

        res = c.post(reverse('api_login'), json_data, content_type='application/json')
        self.assertEquals(res.status_code, 200)

    def test_signup_twice(self):
        c = Client()

        data = {'email': 'test@test.com', 'password': 'password'}
        json_data = json.dumps(data)
        res = c.post(reverse('api_signup'), json_data, content_type='application/json')
        self.assertEquals(res.status_code, 200)

        data = {'email': 'test@test.com', 'password': 'password'}
        json_data = json.dumps(data)
        res = c.post(reverse('api_signup'), json_data, content_type='application/json')
        self.assertEquals(res.status_code, 400)

    def test_lost_password(self):
        c = Client()

        data = {'email': 'test@test.com'}
        json_data = json.dumps(data)
        res = c.post(reverse('api_lost_password'), json_data, content_type='application/json')
        self.assertEquals(res.status_code, 404)
