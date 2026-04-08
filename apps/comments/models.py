import uuid
from django.db import models
from apps.users.models import User
from apps.posts.models import Post
from apps.common.models import BaseModel


class Comment(BaseModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,)

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        editable=False,
        verbose_name="Post ID",
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        editable=False,
        related_name="comments",
        verbose_name="Author ID",
    )

    comment = models.TextField(max_length=2000)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"


