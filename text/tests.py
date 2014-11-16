import json

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client

import settings as text_settings
import tasks
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
        url = 'http://jbl42.com/'

        text = Text.objects.create(url=url, user=self.user)
        text.parse()


class TestTask(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', is_active=True)
        self.user.set_password('password')
        self.user.save()

    def test_task(self):
        c = Client()
        c.login(username='user', password='password')

        url = reverse('api_text_analyze')
        data = {
            'url': 'http://jbl42.com'
        }
        res = c.post(url, json.dumps(data), content_type='application/json')
        self.assertEquals(res.status_code, 200)
        data = json.loads(res.content)
        text = Text.objects.get(task_id=data.get('id'))
        self.assertEquals(text.status, text_settings.TEXT_STATUS_FINISHED)

        url = reverse('api_texts')
        res = c.get(url, content_type='application/json')
        self.assertEquals(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEquals(data.get('count'), 1)

        url = reverse('api_text', args=[text.task_id])
        res = c.get(url, content_type='application/json')
        self.assertEquals(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEquals(data.get('id'), text.task_id)

    def test_forbidden_urls(self):
        c = Client()
        c.login(username='user', password='password')

        url = reverse('api_text_analyze')
        data = {
            'url': 'http://localhost'
        }
        res = c.post(url, json.dumps(data), content_type='application/json')
        self.assertEquals(res.status_code, 400)

        data = {
            'url': 'https://localhost'
        }
        res = c.post(url, json.dumps(data), content_type='application/json')
        self.assertEquals(res.status_code, 400)

        data = {
            'url': 'http://127.0.0.1'
        }
        res = c.post(url, json.dumps(data), content_type='application/json')
        self.assertEquals(res.status_code, 400)

        data = {
            'url': 'https://127.0.0.1'
        }
        res = c.post(url, json.dumps(data), content_type='application/json')
        self.assertEquals(res.status_code, 400)
