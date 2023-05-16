from django.db import models
from datetime import datetime


class Event(models.Model):
    nome = models.CharField(default="", max_length=200)
    info = models.TextField(default="")
    img = models.CharField(default="", max_length=200)
    data = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.id) + " - " + self.title
