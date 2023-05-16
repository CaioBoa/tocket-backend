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
def poke_user(request):
    user = request.user
    try:
        usuario = Usuario.objects.get(user=user)
    except usuario.DoesNotExist:
        raise Http404()
    
    events = usuario.events.all()
    events_names = ""
    for event in events:
        if events_names == "":
            events_names += ((event.nome))
        else:
            events_names += (", " + (event.nome))
    question = "Me envie uma resposta associando a seguinte lista de eventos: {" + events_names + "} com um pokemon, além de duas características dele que contribuem para tal associação. A resposta deve ser enviada no seguinte modelo exato contendo apenas 3 palavras: (pokemon): (característica 1)/(característica 2) \n Exemplo: Pikachu: elétrico/fofo"
    print(events_names)
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
    
    counter = 0

    while True:
        response = requests.post(url, json=payload, headers=headers)
        content = response.json()["choices"][0]["message"]["content"]
        counter += 1
        print(content)
        if (":" in content) and ("/" in content):
                pokemon = content.split(":")[0]
                pokemon = pokemon.replace(" ", "").lower()
                c1 = content.split(":")[1].split("/")[0]
                c1 = c1.replace(" ", "").lower()
                c2 = content.split(":")[1].split("/")[1].split(".")[0]
                c2 = c2.replace(" ", "").lower()
                png = "https://img.pokemondb.net/sprites/brilliant-diamond-shining-pearl/normal/" + pokemon + ".png"

                ret = {
                    "pokemon": pokemon,
                    "c1": c1,
                    "c2": c2,
                    "png": png
                }
                return Response(ret)
        if counter == 3:
            return Response(status=204)

@api_view(['GET'])
def poke_event(request):
    event = request.data['nome_evento']
    question = "Me envie uma resposta associando o seguinte evento: " + event + " com um pokemon, além de duas características dele que contribuem para tal associação. A resposta deve ser enviada no seguinte modelo exato contendo apenas 3 palavras: (pokemon): (característica 1)/(característica 2) \n Exemplo: Pikachu: avassalador/fofo"
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
    
    counter = 0

    while True:
        response = requests.post(url, json=payload, headers=headers)
        content = response.json()["choices"][0]["message"]["content"]
        counter += 1
        print(content)
        if (":" in content) and ("/" in content):
                pokemon = content.split(":")[0]
                pokemon = pokemon.replace(" ", "").lower()
                c1 = content.split(":")[1].split("/")[0]
                c1 = c1.replace(" ", "").lower()
                c2 = content.split(":")[1].split("/")[1].split(".")[0]
                c2 = c2.replace(" ", "").lower()
                png = "https://img.pokemondb.net/sprites/brilliant-diamond-shining-pearl/normal/" + pokemon + ".png"

                ret = {
                    "pokemon": pokemon,
                    "c1": c1,
                    "c2": c2,
                    "png": png
                }
                return Response(ret)
        if counter == 3:
            return Response(status=204)

