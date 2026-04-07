import uuid

from django.db import models
from apps.users.models import User

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

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

    content = models.TextField()

    def __str__(self):
        return self.title




