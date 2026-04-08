import uuid

from django.db import models
from apps.users.models import User
from apps.common.models import BaseModel


class Post(BaseModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Author'
    )

    title = models.CharField(
        max_length=255,
        verbose_name='Title'
    )

    content = models.TextField(
        max_length=10000,
        verbose_name='Content'
    )

    def __str__(self):
        return self.title




