from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from .models import Event
from .serializers import EventSerializer

@api_view(['GET', 'POST'])
def events(request):
    try:
        event = Event.objects.all()
    except Event.DoesNotExist:
        raise Http404()
    serialized_event = EventSerializer(event, many=True)
    return Response(serialized_event.data)