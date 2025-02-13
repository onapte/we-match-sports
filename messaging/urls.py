from django.urls import path
from . import views

app_name = 'messaging-service'

urlpatterns = [
    path('chats/', views.view_chats, name='chatsList'),
    path('chats/pvfq', views.view_chat, name='chatWindow'),
    path('chats/send', views.send_message, name='send_chat'),
    path('chats/user-messages/<str:user_id>', views.get_user_messages, name='user-messages'),
    path('chats/test-send', views.test_send_message, name='test_mess')
]