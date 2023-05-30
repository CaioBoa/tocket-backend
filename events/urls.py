from django.urls import path

from . import views

urlpatterns = [
    path('events/', views.events, name='events'),
    path('events/<int:id>/', views.event, name='event'),
    # path('token/', views.get_token),
    path('users/', views.user),
    path('users/event/', views.user_event),
    path('poke/user/', views.poke_user),
    path('poke/event/<str:event>/', views.poke_event),
    path('poke/get/', views.poke),
]