from django.urls import path

from . import views

urlpatterns = [
    path('events/', views.events, name='events'),
    path('event/<str:nome_evento>/', views.event, name='event'),
    path('token/', views.get_token),
    path('users/', views.user),
    path('users/event/', views.user_event),
    path('api/', views.gpt),
]