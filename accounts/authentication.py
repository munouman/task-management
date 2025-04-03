# accounts/authentication.py

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()  # This will refer to accounts.CustomUser

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)  # Use the custom user model
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
