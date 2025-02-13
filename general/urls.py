from django.urls import path
from . import views

app_name = 'general'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/connection-requests', views.connection_request, name='connection-requests'),
    path('profile/answer-connection-req', views.answer_connection_req, name='answer-request'),
    path('public-rooms/', views.public_rooms, name='public_rooms'),
    path('room/<slug:room_name>/', views.room_detail, name='room_detail'),
]