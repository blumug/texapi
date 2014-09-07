import tweepy
import time
import json
import urllib

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings

from rest_framework import serializers

from core import exceptions
from core.utils import generate_username
from api_users.models import ApiUser


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    password = serializers.CharField(required=False)

    facebook_id = serializers.CharField(required=False)
    facebook_token = serializers.CharField(required=False)

    twitter_id = serializers.CharField(required=False)
    twitter_screen_name = serializers.CharField(required=False)
    twitter_token = serializers.CharField(required=False)
    twitter_token_secret = serializers.CharField(required=False)

    def _download_facebook_profile(self, token):
        facebook_profile = json.load(urllib.urlopen("https://graph.facebook.com/me?" + urllib.urlencode(dict(access_token=token))))
        if not facebook_profile:
            raise exceptions.CommunicationErrorException('LoginResponseFacebookNotFound', 'facebook profile unreachable')

        if 'error' in facebook_profile:
            raise exceptions.CommunicationErrorException('LoginResponseFacebookNotFound', 'facebook profile unreachable')

        if 'id' not in facebook_profile:
            raise exceptions.CommunicationErrorException('LoginResponseFacebookNotFound', 'facebook profile unreachable')

        return facebook_profile

    def validate(self, attrs):
        email = attrs.get('email')

        password = attrs.get('password')

        facebook_id = attrs.get('facebook_id')
        facebook_token = attrs.get('facebook_token')

        twitter_id = attrs.get('twitter_id')
        twitter_screen_name = attrs.get('twitter_screen_name')
        twitter_token = attrs.get('twitter_token')
        twitter_token_secret = attrs.get('twitter_token_secret')

        if email and password:
            return self.authenticate_password(attrs, email, password)
        if email and facebook_token and facebook_id:
            return self.authenticate_facebook(attrs, email, facebook_id, facebook_token)
        if twitter_token and twitter_id and twitter_token_secret and twitter_screen_name:
            return self.authenticate_twitter(attrs, twitter_id, twitter_token, twitter_token_secret, twitter_screen_name)
        raise exceptions.MissingParameterException('Must include "email" and "password"', 'missing parameter')

    def authenticate_password(self, attrs, email, password):
        user = authenticate(username=email, password=password)

        if user:
            if not user.is_active:
                raise exceptions.UnauthorizedException('LoginResponseAccountDisabled', 'account disabled')
            attrs['user'] = user
            return attrs
        else:
            raise exceptions.UnauthorizedException('LoginResponseWrongCredentials', 'unauthorized')

    def authenticate_facebook(self, attrs, email, facebook_id, facebook_token):
        max_retry = 3
        retry = 0
        while retry < max_retry:
            facebook_profile = self._download_facebook_profile(facebook_token)
            if facebook_profile is not None:
                break
            time.sleep(1)
            retry += 1

        if not facebook_profile:
            raise exceptions.CommunicationErrorException('LoginResponseFacebookNotFound', 'facebook unreachable')

        try:
            api_user = ApiUser.objects.get(facebook_id=facebook_id)
            user = api_user.user
            api_user.facebook_token = facebook_token
            user.email = email
            user.first_name = attrs.get('first_name')
            user.last_name = attrs.get('last_name')
            api_user.save()
            attrs['user'] = user
            return attrs
        except ApiUser.DoesNotExist:
            if email:
                if User.objects.filter(email=email, api_user__isnull=False).count() > 0:
                    raise exceptions.DocumentAlreadyExistsException('SignupResponseExistsAlready', 'already exists')

            user = User.objects.create(username=generate_username())
            user.email = email
            user.first_name = attrs.get('first_name', '')
            user.last_name = attrs.get('last_name', '')
            user.save()

            api_user = ApiUser(user=user)
            api_user.facebook_id = facebook_id
            api_user.facebook_token = facebook_token
            api_user.save()

            attrs['user'] = user
            return attrs

    def authenticate_twitter(self, attrs, twitter_id, twitter_token, twitter_token_secret, twitter_screen_name):
        auth = tweepy.OAuthHandler(settings.TWITTER_APP_CONSUMER_KEY, settings.TWITTER_APP_CONSUMER_SECRET)
        auth.set_access_token(twitter_token, twitter_token_secret)
        api = None
        try:
            api = tweepy.API(auth)
        except:
            raise exceptions.UnauthorizedException('LoginResponseWrongCredentials', 'unauthorized')

        max_retry = 3
        retry = 0
        res = None
        while retry < max_retry:
            try:
                res = api.verify_credentials()
                if res:
                    break
            except:
                pass
            time.sleep(1)
            retry += 1

        if (not res) or (res is False):
            raise exceptions.CommunicationErrorException('LoginResponseTwitterNotFound', 'twitter unreachable')
        if res.id != int(twitter_id):
            raise exceptions.UnauthorizedException('LoginResponseWrongCredentials', 'unauthorized')

        try:
            api_user = ApiUser.objects.get(twitter_id=twitter_id)
            user = api_user.user
            api_user.twitter_token = twitter_token
            api_user.twitter_token_secret = twitter_token_secret
            api_user.twitter_screen_name = twitter_screen_name
            user.first_name = attrs.get('first_name', '')
            user.last_name = attrs.get('last_name', '')
            api_user.save()
            attrs['user'] = user
            return attrs
        except ApiUser.DoesNotExist:
            user = User.objects.create(username=generate_username())
            user.first_name = attrs.get('first_name', '')
            user.last_name = attrs.get('last_name', '')
            user.save()

            api_user = ApiUser(user=user)
            api_user.twitter_id = twitter_id
            api_user.twitter_token = twitter_token
            api_user.twitter_token_secret = twitter_token_secret
            api_user.twitter_screen_name = twitter_screen_name
            api_user.save()

            attrs['user'] = user
            return attrs


class SignupSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            if User.objects.filter(email=email, api_user__isnull=False).count() > 0:
                raise exceptions.DocumentAlreadyExistsException('SignupResponseExistsAlready', 'already exists')

            user = User.objects.create(email=email, username=generate_username(), is_active=True, first_name=attrs.get('first_name', ''), last_name=attrs.get('last_name', ''))
            ApiUser.objects.create(user=user)
            user.set_password(password)
            user.save()

            user = authenticate(username=email, password=password)

            if user:
                if not user.is_active:
                    raise exceptions.UnauthorizedException('LoginResponseAccountDisabled', 'account disabled')
                attrs['user'] = user
                return attrs
            else:
                raise exceptions.UnauthorizedException('LoginResponseWrongCredentials', 'unauthorized')
        else:
            raise exceptions.MissingParameterException('Must include "email" and "password"', 'missing parameter')


class ApiUserSerializer(serializers.ModelSerializer):
    userid = serializers.SerializerMethodField('get_username')
    email = serializers.SerializerMethodField('get_email')
    first_name = serializers.SerializerMethodField('get_first_name')
    last_name = serializers.SerializerMethodField('get_last_name')

    def get_username(self, api_user):
        return api_user.user.username

    def get_email(self, api_user):
        return api_user.user.email

    def get_first_name(self, api_user):
        return api_user.user.first_name

    def get_last_name(self, api_user):
        return api_user.user.last_name

    class Meta:
        model = ApiUser
        fields = ('userid', 'email', 'first_name', 'last_name')


class LostPasswordSerializer(serializers.Serializer):
    email = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')

        if email:
            if User.objects.filter(email=email, api_user__isnull=False, is_active=True).count() == 0:
                raise exceptions.DocumentDoesNotExistException('LoginResponseWrongCredentials', 'does not exist')

            user = User.objects.get(email=email, api_user__isnull=False)
            attrs['user'] = user
            return attrs

        else:
            raise exceptions.MissingParameterException('Must include "email"', 'missing parameter')
