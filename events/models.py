from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Event(models.Model):
    nome = models.CharField(default="", max_length=200)
    info = models.TextField(default="")
    img = models.CharField(default="", max_length=200)
    data = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.id) + " - " + self.nome

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    events = models.ManyToManyField(Event, related_name='events')