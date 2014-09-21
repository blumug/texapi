import uuid
from django.contrib.auth.models import User


def generate_username():
    """Helper function to generate a unique random username """
    candidate = uuid.uuid4().hex[:30]
    if User.objects.filter(username=candidate).count() > 0:
        generate_username()
    return candidate
