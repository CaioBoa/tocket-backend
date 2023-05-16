from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from .models import Event, Usuario
from .serializers import EventSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import requests

@api_view(['GET'])
def events(request):
    try:
        events = Event.objects.all()
    except Event.DoesNotExist:
        raise Http404()
    serialized_events = EventSerializer(events, many=True)
    return Response(serialized_events.data)

@api_view(['GET'])
def event(request, nome_evento):
    try:
        event = Event.objects.get(nome=nome_evento)
    except Event.DoesNotExist:
        raise Http404()
    serialized_event = EventSerializer(event)
    return Response(serialized_event.data)

@api_view(['POST'])
def get_token(request):
    try:
        if request.method == 'POST':
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return JsonResponse({"token":token.key})
            else:
                return HttpResponseForbidden()
    except:
        return HttpResponseForbidden()
    
@api_view(['POST'])
def user(request):
    if request.method == 'POST':
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']

        user = User.objects.create_user(username, email, password)
        user.save()
        usuario = Usuario(user=user)
        usuario.save()
        return Response(status=204)
    
@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_event(request):
    user = request.user
    try:
        usuario = Usuario.objects.get(user=user)
    except usuario.DoesNotExist:
        raise Http404()
    
    if request.method == 'POST':
        event = Event.objects.get(nome=request.data['nome_evento'])
        usuario.events.add(event)
        return Response(status=204)
    elif request.method == 'DELETE':
        event = Event.objects.get(nome=request.data['nome_evento'])
        usuario.events.remove(event)
        return Response(status=204)
    elif request.method == 'GET':
        events = usuario.events.all()
        serialized_events = EventSerializer(events, many=True)
        return Response(serialized_events.data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gpt(request):
    user = request.user
    try:
        usuario = Usuario.objects.get(user=user)
    except usuario.DoesNotExist:
        raise Http404()
    
    events = usuario.events.all()
    events_names = ""
    for event in events:
        events_names += ((event.nome) + ", ")
    question = "Baseado em tais nomes de eventos: " + events_names + "me diga o nome de um Pokemon que de alguma forma remeta a tais nomes e duas características que colaboram para tal associação. Sua reposta deve ser dada na seguinte formatação: (Pokemon) : (Característica 1), (Característica 2)"

    url = "https://openai80.p.rapidapi.com/chat/completions"

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "ee86e4df16msh1a98ded04575ec5p1d27a0jsn74e1538c0c2e",
        "X-RapidAPI-Host": "openai80.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.json())
    print(response.json()["choices"][0]["message"]["content"])
    return Response(response.json())
