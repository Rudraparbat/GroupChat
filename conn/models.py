from django.db import models

from django.db import models
from django.contrib.auth.models import User

class chatroom(models.Model) :
    ROOM_TYPE_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    name = models.TextField(max_length=25)
    bio = models.TextField(max_length=200)
    room_id = models.CharField(max_length=4)
    room_type = models.CharField(
        max_length=10,
        choices=ROOM_TYPE_CHOICES,
        default='public',
    )
    participants = models.ManyToManyField(User ,blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta :
        ordering = ['-updated' , '-created']
    def __str__(self):
        return self.name
class msg(models.Model) :
    host = models.ForeignKey(User ,on_delete=models.CASCADE ,default=True)
    room = models.ForeignKey(chatroom,on_delete=models.CASCADE ,null=True)
    body = models.TextField(max_length=255)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta :
        ordering = ['-updated' , '-created']
    def __str__(self) :
        return self.body[0:10]
