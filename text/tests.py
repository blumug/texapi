import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client

from models import Text


class TestApi(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', is_active=True)
        self.user.set_password('password')
        self.user.save()

    def test_analyze_text(self):
        url = reverse('api_text_analyze')
        c = Client()

        data = {
            'url': 'http://google.fr'
        }
        res = c.post(url, json.dumps(data), content_type='application/json')
        self.assertEquals(res.status_code, 401)


class TestParse(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', is_active=True)
        self.user.set_password('password')
        self.user.save()

    def test_parse(self):
        url = 'http://libnui.github.io/nui3/'

        text = Text.objects.create(url=url, user=self.user)
        text.parse()
