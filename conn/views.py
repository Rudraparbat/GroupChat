from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate , login , logout  
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import re
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
        rooms = chatroom.objects.all()
        b = rooms.count()
    return render(request , 'index.html' , {'room':rooms , 'b':b})
@login_required(login_url='li')
def rooms(request , pk) :
    ct = chatroom.objects.get(id=pk)
    if(str(request.user) == str(ct.name)) :
        pasr = 'ok'
    else :
        pasr = 'no'
    if request.method =='POST' :
        pas = request.POST.get('pa')
        if pas == ct.password :
            return render(request , 'room.html' ,{'ct':ct , 'pasr':pasr})
        else :
            return HttpResponse("sorry you cant enter this room cause your enterd password is wrong my friend")
    return render(request , 'password.html',{'cts':ct})
@login_required(login_url='li')
def createroom(request):
    form = roomfrom()
    if request.method=='POST' :
        vform= roomfrom(request.POST)
        if vform.is_valid() :
            vform.save()
            return redirect('main')
    return render(request , 'from.html' ,{'from' : form})
def updatedr(request , pk) :
    upfor = chatroom.objects.get(id=pk)
    ufor = roomfrom(instance=upfor)
    if request.method == 'POST':
        fo = roomfrom(request.POST , instance=upfor)
        if fo.is_valid() :
            fo.save()
            return redirect('main')
    return render(request , 'from.html' ,{'from' : ufor})
def deleter(request,pk) :
    dfor = chatroom.objects.get(id=pk)
    if request.method == 'POST':
        dfor.delete()
        return redirect(main)
    return render(request , 'delete.html')
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
            response.set_cookie('username', user.username, max_age=3600, secure=True, httponly=True)
            return response
        else :
            return redirect('li')
    return render(request , 'logge.html')
def getout(request) :
    logout(request)
    response =  redirect('/')
    response.delete_cookie('username')
    return response
@login_required(login_url='li')
def chatting(request,pk) :
    roomca = chatroom.objects.get(id=pk)
    msgr = roomca.msg_set.all()
    roomca.participants.add(request.user)
    parts = roomca.participants.all()
    print(parts)
    user =  request.COOKIES.get('username')
    if(user) :
        return render(request , 'chat.html' ,{'usr': user ,'past':parts})
    else :
        return redirect('li')
    