import uuid

from django.db import models
from apps.users.models import User
from apps.posts.models import Post

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Comment(BaseModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4(),
        editable=False,)

    post_id = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        editable=False,
        verbose_name="Post ID",
    )

    author_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        editable=False,
        related_name="comments",
        verbose_name="Author ID",
    )

    content = models.TextField()

    def __str__(self):
        return f"Comment by {self.author_id} on {self.post_id}"


