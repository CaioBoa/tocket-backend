from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from .models import Event, EventUser
from .serializers import EventSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import requests
import json
import time
import os
import openai

@api_view(['GET'])
def events(request):
    try:
        events = Event.objects.all()
    except Event.DoesNotExist:
        raise Http404()
    serialized_events = EventSerializer(events, many=True)
    return Response(serialized_events.data)

@api_view(['GET'])
def event(request, id):
    try:
        event = Event.objects.get(id=id)
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
        usuario = EventUser(user=user)
        usuario.save()
        return Response(status=204)
    
@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_event(request):
    user = request.user
    try:
        usuario = EventUser.objects.get(user=user)
    except usuario.DoesNotExist:
        raise Http404()
    
    if request.method == 'POST':
        event = Event.objects.get(name=request.data['event_name'])
        usuario.events.add(event)
        return Response(status=204)
    elif request.method == 'DELETE':
        event = Event.objects.get(name=request.data['event_name'])
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
        usuario = EventUser.objects.get(user=user)
    except usuario.DoesNotExist:
        raise Http404()
    
    Key = "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"
    openai.api_key = Key
    events = usuario.events.all()
    events_names = ""
    for event in events:
        if events_names == "":
            events_names += ((event.name))
        else:
            events_names += (", " + (event.name))
            
    question = "Me envie uma resposta associando a(s) seguintes palavras: {" + events_names + "} com um pokemon, além de duas características dele que contribuem para tal associação. A resposta deve ser enviada no seguinte modelo exato contendo apenas 3 palavras: (pokemon): (característica 1)/(característica 2) \n Exemplo: Pikachu: pilantra/fofo"
    counter = 0

    while True:
        try:
            completion = openai.Completion.create(
                model="text-davinci-003",
                prompt= question,
                max_tokens=30,
                temperature=0.5
            )
            content = completion.choices[0]["text"]
            counter += 1
            if (":" in content) and ("/" in content):
                png = ""
                pokemon = content.replace("\n", "")
                pokemon = pokemon.split(":")[0]
                pokemon = pokemon.replace(" ", "").lower()
                c1 = content.split(":")[1].split("/")[0]
                c1 = c1.replace(" ", "").lower()
                c2 = content.split(":")[1].split("/")[1].split(".")[0]
                c2 = c2.replace(" ", "").lower()

                with open('pokemon.json', 'r') as f:
                    pokemons = json.load(f)
                for p in pokemons:
                    if p["slug"] == pokemon:
                        png = p["ThumbnailImage"]

                        ret = {
                            "pokemon": pokemon,
                            "c1": c1,
                            "c2": c2,
                            "png": png,
                            "Status": "OK"
                        }
                        return Response(ret)
                    
                ret = {
                    "pokemon": "snorlax",
                    "c1": "tranquilo",
                    "c2": "maneiro",
                    "png": "https://assets.pokemon.com/assets/cms2/img/pokedex/detail/143.png",
                    "Status": "Pokemon not Found"
                }    
                
        except:
            counter += 1
            print("Erro")
            
        
        if counter == 5:
            ret = {
                    "pokemon": "articuno",
                    "c1": "posturado",
                    "c2": "gelado",
                    "png": "https://assets.pokemon.com/assets/cms2/img/pokedex/detail/144.png",
                    "Status": "Counter Exceeded"
                }
            return Response(ret)

@api_view(['GET'])
def poke_event(request):
    event = request.data['event_name']
    #tivita = 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
    Key = "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"
    openai.api_key = Key
    question = "Me envie uma resposta associando a(s) seguintes palavras: {" + event + "} com um pokemon, além de duas características dele que contribuem para tal associação. A resposta deve ser enviada no seguinte modelo exato contendo apenas 3 palavras: (pokemon): (característica 1)/(característica 2) \n Exemplo: Pikachu: pilantra/fofo"
    
    counter = 0

    while True:
        try:
            completion = openai.Completion.create(
                model="text-davinci-003",
                prompt= question,
                max_tokens=30,
                temperature=1
            )
            print(completion)
            content = completion.choices[0]["text"]
            counter += 1
            if (":" in content) and ("/" in content):
                png = ""
                pokemon = content.replace("\n", "")
                pokemon = pokemon.split(":")[0]
                pokemon = pokemon.replace(" ", "").lower()
                c1 = content.split(":")[1].split("/")[0]
                c1 = c1.replace(" ", "").lower()
                c2 = content.split(":")[1].split("/")[1].split(".")[0]
                c2 = c2.replace(" ", "").lower()

                with open('pokemon.json', 'r') as f:
                    pokemons = json.load(f)
                for p in pokemons:
                    if p["slug"] == pokemon:
                        png = p["ThumbnailImage"]
                        ret = {
                            "pokemon": pokemon,
                            "c1": c1,
                            "c2": c2,
                            "png": png,
                            "Status": "OK"
                        }
                        return Response(ret)
                    
                ret = {
                    "pokemon": "foongus",
                    "c1": "toxico",
                    "c2": "charmoso",
                    "png": "https://assets.pokemon.com/assets/cms2/img/pokedex/detail/590.png",
                    "Status": "Pokemon not Found"
                } 
            else:
                print("Error in content")   
                
        except:
            counter += 1
            print("Error in completion")
            
        
        if counter == 5:
            ret = {
                    "pokemon": "pichu",
                    "c1": "pilantra",
                    "c2": "curioso",
                    "png": "https://assets.pokemon.com/assets/cms2/img/pokedex/detail/172.png",
                    "Status": "Counter Exceeded"
                }
            print("Counter Exceeded")
            return Response(ret)

@api_view(['GET'])
def poke(request):
    url = "https://pokedex2.p.rapidapi.com/pokedex/uk"

    headers = {
        "X-RapidAPI-Key": "ee86e4df16msh1a98ded04575ec5p1d27a0jsn74e1538c0c2e",
        "X-RapidAPI-Host": "pokedex2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    print(response.json())

    with open("pokemon.json", "w") as outfile:
        json.dump(response.json(), outfile)

