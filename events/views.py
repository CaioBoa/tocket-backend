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

# @api_view(['POST'])
# def get_token(request):
#     try:
#         if request.method == 'POST':
#             username = request.data['username']
#             password = request.data['password']
#             user = authenticate(username=username, password=password)

#             if user is not None:
#                 token, created = Token.objects.get_or_create(user=user)
#                 return JsonResponse({"token":token.key})
#             else:
#                 return HttpResponseForbidden()
#     except:
#         return HttpResponseForbidden()
    
@api_view(['POST'])
def user(request):
    if request.method == 'POST':
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        eventUsers = EventUser.objects.all()
        for eventUser in eventUsers:
            if eventUser.username == username:
                return Response(status=409)

        eventUser = EventUser(username=username, email=email, password=password)
        eventUser.save()
        # usuario = EventUser(user=user)
        # usuario.save()

        return Response(status=204)
    
@api_view(['GET', 'POST', 'DELETE'])
def user_event(request):
    # print("----------------------", request)
    # password = request.headers['Password']
    password = request.data['password']

    try:
        event_user = EventUser.objects.get(password=password)
    except event_user.DoesNotExist:
        raise Http404()
    
    if request.method == 'POST':
        try:
            event_id = int(request.data['event_id'])
            event = Event.objects.get(id=event_id)
            event_user.events.add(event)
            print(event_user.events.all())
            return Response(status=204)
        except:
    # if request.method == 'GET':
            events = event_user.events.all()
            serialized_events = EventSerializer(events, many=True)
            return Response(serialized_events.data)
    
    elif request.method == 'DELETE':
        event = Event.objects.get(id=request.data['event_id'])
        event_user.events.remove(event)
        print(event_user.events.all())
        return Response(status=204)

@api_view(['GET'])
def poke_event(request, event):
    useKey = True
    print(event)
    Key1 = "sk-I9C6NzzI0alONinaagsOT3Blbk"
    Key2 = "FJJtpasS29MdYUWYZR0DUT"
    if useKey:
        Key = Key1 + Key2
    else:
        Key = ""

    openai.api_key = Key
    question = "Me envie uma resposta associando a(s) seguintes palavras: {" + event + "} com um pokemon, além de dois adjetivos que contribuem para tal associação. A resposta deve ser enviada no seguinte modelo exato contendo apenas 3 palavras: (pokemon): (adjetivo 1)/(adjetivo 2) \n Exemplo: Pikachu: pilantra/fofo"
    
    counter = 0

    while True:
        try:
            completion = openai.Completion.create(
                model="text-davinci-003",
                prompt= question,
                max_tokens=30,
                temperature=0.6
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

