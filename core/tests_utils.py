import json

from django.contrib.auth.models import User
from django.test.client import Client
from django.core.urlresolvers import reverse

from rest_framework.authtoken.models import Token

from api_users.models import AppUser


def generate_api_user(username='user', email='test@test.com', password='password', login=True):
    """Generate app user

    Args:
        username: username
        email: email
        password: password
        login: if set to True, a login query is made

    Returns:
        user, token, header
    """
    token = None
    header = None
    user = User.objects.create(
        username=username, email=email, is_active=True)
    AppUser.objects.create(user=user)
    user.set_password('password')
    user.save()

    c = Client()

    data = {
        'email': 'test@test.com',
        'password': 'password',
    }
    json_data = json.dumps(data)
    if login is True:
        res = c.post(reverse('api_login'),
                     json_data, content_type='application/json')
        data = json.loads(res.content)
        token = Token.objects.get(user=user).key
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
    return user, token, header
