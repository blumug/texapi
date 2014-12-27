# -*- coding: utf-8 -*-
import json
import os

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client

from mock import patch

import settings as text_settings
import tasks
from models import Text


class TestApi(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', is_active=True)
        self.user.set_password('password')
        self.user.save()

    def mock_requests_get(self, *args, **kwargs):
        class RequestResponse(object):
            """
            Fake requests response object
            """
            status_code = 200

            @property
            def text(self):
                html_filename = os.path.join(os.path.dirname(__file__), 'fixtures/google.html')
                with open(html_filename, "r") as html_file:
                    return html_file.read()

        return RequestResponse()

    @patch('requests.get')
    def test_analyze_text(self, mock_request):
        mock_request.side_effect = self.mock_requests_get
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

    def test_get_base_url(self):
        url = 'https://medium.com/the-right-tool-for-the-right-job/email-patterns-for-web-apps-c6303f3b6e8c'
        text = Text.objects.create(url=url, user=self.user)
        self.assertEquals("https://medium.com", text._get_base_url())

    def mock_requests_get(self, *args, **kwargs):
        class RequestResponse(object):
            """
            Fake requests response object
            """
            status_code = 200

            @property
            def text(self):
                html_filename = os.path.join(os.path.dirname(__file__), 'fixtures/medium.html')
                with open(html_filename, "r") as html_file:
                    return html_file.read()

        return RequestResponse()

    @patch('requests.get')
    def test_parse(self, mock_request):
        mock_request.side_effect = self.mock_requests_get

        url = 'https://medium.com/the-right-tool-for-the-right-job/email-patterns-for-web-apps-c6303f3b6e8c'

        text = Text.objects.create(url=url, user=self.user)
        text.parse()


class TestImages(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', is_active=True)
        self.user.set_password('password')
        self.user.save()

    def test_get_base_url(self):
        url = 'https://medium.com/the-right-tool-for-the-right-job/email-patterns-for-web-apps-c6303f3b6e8c'
        text = Text.objects.create(url=url, user=self.user)
        self.assertEquals("https://medium.com", text._get_base_url())

    def mock_requests_get(self, *args, **kwargs):
        class RequestResponse(object):
            """
            Fake requests response object
            """
            status_code = 200

            @property
            def text(self):
                html_filename = os.path.join(os.path.dirname(__file__), 'fixtures/relative_images.html')
                with open(html_filename, "r") as html_file:
                    return html_file.read()

        return RequestResponse()

    @patch('requests.get')
    def test_parse(self, mock_request):
        mock_request.side_effect = self.mock_requests_get

        url = 'https://foo.com/bar/meuh.html'

        text = Text.objects.create(url=url, user=self.user)
        text.parse()
        self.assertTrue('/foo/bar/test.png' in text.raw)
        self.assertTrue('boo.png' in text.raw)
        self.assertTrue('https://foo.com/boo.png' in text.readable)
        self.assertTrue('https://foo.com/foo/bar/test.png' in text.readable)


class TestTitle(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', is_active=True)
        self.user.set_password('password')
        self.user.save()

    def test_get_base_url(self):
        url = 'https://medium.com/the-right-tool-for-the-right-job/email-patterns-for-web-apps-c6303f3b6e8c'
        text = Text.objects.create(url=url, user=self.user)
        self.assertEquals("https://medium.com", text._get_base_url())

    def mock_requests_get(self, *args, **kwargs):
        class RequestResponse(object):
            """
            Fake requests response object
            """
            status_code = 200

            @property
            def text(self):
                html_filename = os.path.join(os.path.dirname(__file__), 'fixtures/title.html')
                with open(html_filename, "r") as html_file:
                    return html_file.read()

        return RequestResponse()

    @patch('requests.get')
    def test_parse(self, mock_request):
        mock_request.side_effect = self.mock_requests_get

        url = 'https://foo.com/bar/meuh.html'

        text = Text.objects.create(url=url, user=self.user)
        text.parse()

        self.assertEquals('This is a title', text.title)


class TestTags(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', is_active=True)
        self.user.set_password('password')
        self.user.save()

    def test_get_base_url(self):
        url = 'https://medium.com/the-right-tool-for-the-right-job/email-patterns-for-web-apps-c6303f3b6e8c'
        text = Text.objects.create(url=url, user=self.user)
        self.assertEquals("https://medium.com", text._get_base_url())

    def mock_requests_get(self, *args, **kwargs):
        class RequestResponse(object):
            """
            Fake requests response object
            """
            status_code = 200

            @property
            def text(self):
                html_filename = os.path.join(os.path.dirname(__file__), 'fixtures/tags.html')
                with open(html_filename, "r") as html_file:
                    return html_file.read()

        return RequestResponse()

    @patch('requests.get')
    def test_parse(self, mock_request):
        mock_request.side_effect = self.mock_requests_get

        url = 'https://foo.com/bar/meuh.html'

        text = Text.objects.create(url=url, user=self.user)
        text.parse()

        self.assertTrue(len(text.tags) > 0)
        self.assertEquals(text.tags, u'informatique emploi apprendre cours programmation développeurs code chrome tutoriel actualité developpement formation article webdesigner')


class TestTask(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', is_active=True)
        self.user.set_password('password')
        self.user.save()

    def mock_requests_get(self, *args, **kwargs):
        class RequestResponse(object):
            """
            Fake requests response object
            """
            status_code = 200

            @property
            def text(self):
                html_filename = os.path.join(os.path.dirname(__file__), 'fixtures/medium.html')
                with open(html_filename, "r") as html_file:
                    return html_file.read()

        return RequestResponse()

    @patch('requests.get')
    def test_task(self, mock_request):
        mock_request.side_effect = self.mock_requests_get

        c = Client()
        c.login(username='user', password='password')

        url = reverse('api_text_analyze')
        data = {
            'url': 'https://medium.com/the-right-tool-for-the-right-job/email-patterns-for-web-apps-c6303f3b6e8c'
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
