import uuid
from django.db import models

from apps.common.models import BaseModel
from apps.posts.models import Post
from apps.users.models import User


class Like(BaseModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="likes",
        verbose_name="User"
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes",
        verbose_name="Post"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_like",
            )
        ]

    def __str__(self):
        return f"{self.user} liked {self.post}"