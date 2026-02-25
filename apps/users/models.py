from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.common.models import TimeStamp, DeleteMixin
from apps.users.managers import UserManager


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

    def __str__(self):
        return self.username


