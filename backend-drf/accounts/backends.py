from django.contrib.auth.backends import BaseBackend
from .models import User


class PhoneBackend(BaseBackend):
    def authenticate(self, request, phone=None, password=None):
        try:
            user = User.objects.get(phone=phone)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None