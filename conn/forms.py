from django.forms import ModelForm
from .models import *

class roomfrom(ModelForm):
    class Meta :
        model = chatroom
        fields = '__all__'
        exclude = ('participants',)