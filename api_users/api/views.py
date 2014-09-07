from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.utils.http import int_to_base36
from django.conf import settings

from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import parsers
from rest_framework import renderers
from rest_framework import permissions
from serializers import LoginSerializer, ApiUserSerializer, SignupSerializer, LostPasswordSerializer

from api_users.models import ApiUser

import datetime


class LoginView(APIView):
    """Login as application user. Returns a token

    Login by email/password:
        {
            "email" : "foo@foo.org",
            "password": "mypassword"
        }

    Login with facebook:
        {
            "email" : "foo@foo.org",
            "facebook_id": "FACEBOOK_ID"
            "facebook_token": "FACEBOOK_TOKEN",
            "first_name": "john",
            "last_name": "doe"
        }

    Login with twitter:
        {
            "email" : "foo@foo.org",
            "twitter_id": "TWITTER_ID",
            "twitter_token": "TWITTER_TOKEN",
            "twitter_token_secret": "TWITTER_TOKEN_SECRET",
            "twitter_screen_name": "johndoe23",
            "first_name": "john",
            "last_name": "doe"
        }

    Returns:
        {'token': 'foo'}
    """
    throttle_classes = ()
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = LoginSerializer
    model = Token

    def get_serializer_class(self):
        return LoginView.serializer_class

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.object['user'])

            if not created:
                # update the created time of the token to keep it valid
                token.created = datetime.datetime.utcnow()
                token.save()

            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
login = LoginView.as_view()


class SignupView(APIView):
    """Signup as application user. Returns a token

    Input:
        {
            "email" : "foo@foo.org",
            "password": "mypassword",
            "first_name": "john",
            "last_name": "doe"
        }

    Returns:
        {'token': 'foo'}
    """
    throttle_classes = ()
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = SignupSerializer
    model = Token

    def get_serializer_class(self):
        return SignupView.serializer_class

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():

            token, created = Token.objects.get_or_create(user=serializer.object['user'])

            if not created:
                # update the created time of the token to keep it valid
                token.created = datetime.datetime.utcnow()
                token.save()

            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
signup = SignupView.as_view()


class MeView(generics.GenericAPIView):
    throttle_classes = ()
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = ApiUserSerializer

    def get(self, request):
        user = request.user
        api_user = ApiUser.objects.get(user=user)
        serializer = self.get_serializer(api_user)
        return Response(serializer.data)
me = MeView.as_view()


class LostPasswordView(APIView):
    """Lost password view

    """
    throttle_classes = ()
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = LostPasswordSerializer
    model = Token

    def get_serializer_class(self):
        return LostPasswordView.serializer_class

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            user = serializer.object['user']
            email = user.email

            opts = {
                'user': user,
                'use_https': request.is_secure(),
                'token_generator': default_token_generator,
                'from_email': email,
                'request': request,
            }
            self.send_reset_password(**opts)

            return Response({'success': True})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_reset_password(self, user, domain_override=None, use_https=False, token_generator=default_token_generator, from_email=None, request=None):
        domain_override = request.META['HTTP_HOST']
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override

        c = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': int_to_base36(user.id),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': use_https and 'https' or 'http',
        }

        subject, body, body_html = self.build_templates(c)
        msg = EmailMultiAlternatives(subject.strip(), body, settings.DEFAULT_FROM_EMAIL, [user.email])
        msg.attach_alternative(body_html, "text/html")
        msg.send()

    def build_templates(self, c):
        context = Context(c)

        subject = render_to_string('api_users/lost_password/subject.txt', context)
        body = render_to_string('api_users/lost_password/body.txt', context)
        body_html = render_to_string('api_users/lost_password/body.html', context)
        return subject, body, body_html
lost_password = LostPasswordView.as_view()
