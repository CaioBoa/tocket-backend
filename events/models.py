from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(default="", max_length=200)
    info = models.TextField(default="")
    img = models.CharField(default="", max_length=200)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.id) + " - " + self.name

class EventUser(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(default="", max_length=200)
    email = models.CharField(default="", max_length=200)
    password = models.CharField(default="", max_length=200)
    events = models.ManyToManyField(Event, related_name='events')

    def __str__(self):
        return str(self.id) + " - " + self.username