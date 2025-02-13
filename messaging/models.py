from django.db import models
from authentication.models import User

class Message(models.Model):
    sender_id = models.CharField(max_length=1000)
    receiver_id = models.CharField(max_length=1000)
    content = models.CharField(max_length=1000)
    timeStamp = models.DateTimeField()

class UserMessagePair(models.Model):
    sender_id = models.CharField(max_length=1000)
    receiver_id = models.CharField(max_length=1000)