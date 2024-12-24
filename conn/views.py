from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate , login , logout  
from django.contrib.auth.decorators import login_required
from .models import *
import re
from .generator import *
from django.core.cache import cache
def home(request) :
    if request.user.is_authenticated :
        return redirect('main')
    return render(request , 'home.html')
def main(request) :
    if request.GET.get('q') != None :
        a = request.GET.get('q')
        rooms = chatroom.objects.filter(name__icontains=a , room_type="public")
        b= rooms.count()
    else :
        rooms = chatroom.objects.filter(room_type="public")
        b = rooms.count()
    return render(request , 'index.html' , {'room':rooms , 'b':b})
@login_required(login_url='li')
def rooms(request , pk) :
    ct = chatroom.objects.get(id=pk)
    return render(request , 'password.html',{'cts':ct})
@login_required(login_url='li')
def createroom(request):
    if request.method=='POST' :
        room_name = request.POST.get('room_name')
        bio = request.POST.get('bio')
        room_id  = PasswordGenerator.generate()
        room_type = request.POST.get('room_types')
        Room = chatroom(host=request.user,name=room_name,bio=bio,room_id=room_id,room_type=room_type)
        Room.save()
        return redirect('main')
    return render(request , 'from.html')
def updatedr(request , pk) :
    upfor = chatroom.objects.get(id=pk)
    ufor = roomfrom(instance=upfor)
    if request.method == 'POST':
        fo = roomfrom(request.POST , instance=upfor)
        if fo.is_valid() :
            fo.save()
            return redirect('main')
    return render(request , 'from.html' ,{'from' : ufor})
def Profile_page(request) :
    user_id = request.COOKIES.get('id')
    if(user_id) :
        user_profile = User.objects.get(id=user_id)
        print(user_profile)
        try :
            rooms_created = chatroom.objects.filter(host=user_profile)
        except :
            rooms_created = None
        return render(request , 'profile.html' , {'user':user_profile,'rooms':rooms_created})
    else :
        return redirect('li')
def signin(request) :
    sihn = UserCreationForm()
    if request.method == 'POST' :
        username = request.POST.get('username')
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if re.match(email_regex,username) :
            mainuser = UserCreationForm(request.POST)
            if mainuser.is_valid() :
                mainuser.save()
                return redirect('li')
            else :
                return redirect('si')
    return render(request , 'signin.html', {'sin':sihn})
def logini(request) :
    if request.user.is_authenticated :
        return redirect('main')
    if request.method == 'POST' :
        username = request.POST.get('us')
        password = request.POST.get('pa')
        user = authenticate(username=username , password=password)
        if user is not None :
            login(request , user)
            response = redirect('main')
            response.set_cookie('id', user.id, max_age=84600, secure=True, httponly=True)
            return response
        else :
            return redirect('li')
    return render(request , 'logge.html')
def getout(request) :
    logout(request)
    response =  redirect('/')
    response.delete_cookie('id')
    response.delete_cookie('chat_id')
    return response

@login_required(login_url='li')
def private_room(request) :
    if request.method == "POST" :
        room_id = request.POST.get('room_key')    
        try :
            rooms = chatroom.objects.get(room_id=room_id,room_type="private")
        except :
            rooms = None
        if rooms :
            chat_id = PasswordGenerator.chat_id_generate() 
            response = redirect('ch',pk=rooms.id)
            response.set_cookie('chat_id', chat_id)
            return response
        else :
            print("room not found")
    return render(request , 'private_room_password.html')

@login_required(login_url='li')
def chatting(request,pk) :
    User_id =  request.COOKIES.get('id')
    try :
        chat_id = request.COOKIES.get('chat_id')
    except :
        chat_id = None
        return redirect('main')
    if(User_id or chat_id is not None) :
        user = User.objects.get(id=User_id)
        try :
            chat_room = chatroom.objects.get(id=pk)
            return render(request , 'chat.html' ,{'room': chat_room , 'user':user})
        except :
            return redirect('rooms',pk=pk)
    else :
        return redirect('li')
