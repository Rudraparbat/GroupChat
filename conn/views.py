from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate , login , logout  
from django.contrib.auth.decorators import login_required
from .models import *
import re
from .generator import *
def home(request) :
    if request.user.is_authenticated :
        return redirect('main')
    return render(request , 'home.html')
def main(request) :
    if request.GET.get('q') != None :
        a = request.GET.get('q')
        rooms = chatroom.objects.filter(name__icontains=a)
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
    user_profile = chatroom.objects.get(id=user_id)
    return render(request , 'profile.html' , {'user':user_profile})
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
            response.set_cookie('id', user.id, max_age=3600, secure=True, httponly=True)
            return response
        else :
            return redirect('li')
    return render(request , 'logge.html')
def getout(request) :
    logout(request)
    response =  redirect('/')
    response.delete_cookie('id')
    return response
@login_required(login_url='li')
def chatting(request,pk) :
    roomca.participants.add(request.user)
    User_id =  request.COOKIES.get('id')
    if(User_id) :
        user = chatroom.objects.get(id=pk)
        return render(request , 'chat.html' ,{'usr': username.host.username })
    else :
        return redirect('li')
    