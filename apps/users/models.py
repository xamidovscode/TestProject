__all__ = (
    'User',
)

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.common.models import TimeStamp, DeleteMixin
from apps.users.managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser, TimeStamp, DeleteMixin):

    first_name = None
    last_name = None
    email = None

    full_name = models.CharField(
        max_length=255, verbose_name='Full Name'
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []


    objects = UserManager()

    def get_tokens_for_user(self):
        refresh = RefreshToken.for_user(self)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def __str__(self):
        return self.username


