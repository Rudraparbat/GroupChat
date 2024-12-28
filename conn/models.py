from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Sweetusers(models.Model) :
    username = models.CharField(max_length=255 , unique=True) 
    email = models.EmailField(max_length=255)
    set_password = models.CharField(max_length=255)
    def __str__(self):
        return self.username


class chatroom(models.Model) :
    ROOM_TYPE_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    host = models.ForeignKey(Sweetusers,on_delete=models.CASCADE,null=True,blank='True' , related_name='Host_chatroom')
    name = models.TextField(max_length=25)
    bio = models.TextField(max_length=200)
    room_id = models.CharField(max_length=8)
    room_type = models.CharField(
        max_length=10,
        choices=ROOM_TYPE_CHOICES,
        default='public',
    )
    participants_count = models.CharField(max_length=255,blank=True ,null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta :
        ordering = ['-updated' , '-created']
    def __str__(self):
        return self.name
