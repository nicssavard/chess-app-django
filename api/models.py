from django.db import models
from django.contrib.auth.models import User
# import string
# import random

class Chat(models.Model):
    participants = models.ManyToManyField(User)

    def __str__(self):
        return f"Chat: {self.id}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User,  on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

# def generate_unique_code():
#     length = 6

#     while True:
#         code = ''.join(random.choices(string.ascii_uppercase, k=length)) # k is the length of the string'
#         if Room.objects.filter(code=code).count() == 0:
#             break
    
#     return code

# # Create your models here.
# class Room(models.Model):
#     code = models.CharField(max_length=8, default='', unique=True)
#     host = models.CharField(max_length=50, unique=True)
#     guest_can_pause = models.BooleanField(null=False, default=False)
#     votes_to_skip = models.IntegerField(null=False, default=1)
#     created_at = models.DateTimeField(auto_now_add=True)


