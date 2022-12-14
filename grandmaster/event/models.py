from django.db import models
from .utils import PathAndHash
from authentication.models import User


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    address = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    cover = models.ImageField(upload_to=PathAndHash('events/covers'), null=True)
    open = models.BooleanField(default=True)
    hidden = models.BooleanField(default=False)
    number = models.IntegerField(default=0)
    members = models.ManyToManyField(User, related_name='events')

    class Meta:
        db_table = 'events'
        ordering = ['number', 'start_date']

    def __str__(self):
        return self.name
