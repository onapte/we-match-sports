from django.urls import path
from . import views

app_name = 'matchmaking'

urlpatterns = [
    path('match-making/', views.find_matched_players, name='match-making'),
]