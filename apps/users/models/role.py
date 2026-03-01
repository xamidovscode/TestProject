__all__ = (
    "Role",
)
from django.db import models

from apps.common.models import TimeStamp


class Role(TimeStamp):
    name = models.CharField(
        verbose_name='Name',
    )

    class Meta:
        db_table = 'roles'
