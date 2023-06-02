from rest_framework import serializers
from .models import Event, EventUser

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'info', 'img', 'date']

class EventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventUser
        fields = ['username', 'email', 'password', 'events']