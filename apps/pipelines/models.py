from django.db import models
from apps.common.models import TimeStamp, DeleteMixin


class Pipeline(TimeStamp, DeleteMixin):
    name = models.CharField(
        max_length=255,
        verbose_name='Pipeline',
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Order',
    )
    background = models.ImageField(
        null=True, blank=True,
        upload_to='pipelines/background',
        verbose_name='Background',
    )

    class Meta:
        db_table = 'pipelines'
        verbose_name = 'Pipeline'
        verbose_name_plural = 'Pipelines'


class Status(TimeStamp, DeleteMixin):

    class StatusChoices(models.IntegerChoices):
        NEW = (0, 'New')
        SUCCESS = (1, 'Success')

    name = models.CharField(
        max_length=255,
        verbose_name='Status name',
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Order',
    )
    deletable = models.BooleanField(
        default=True,
        verbose_name='Deleteable',
    )

