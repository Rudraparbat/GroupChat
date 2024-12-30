from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate , login , logout  
from django.contrib.auth.decorators import login_required
from .models import *
from .generator import *

def home(request) :
    try :
        tokens = request.COOKIES.get('access_token')
    except :
        tokens = None
    if tokens :
        return redirect('main')
    return render(request , 'home.html')
def main(request) :
    try :
        tokens = request.COOKIES.get('access_token')
        response = PasswordGenerator.decode_token(tokens)
        username = response['username']
    except :
        return redirect('li')
    if request.GET.get('q') != None :
        a = request.GET.get('q')
        rooms = chatroom.objects.filter(name__icontains=a , room_type="public")
        b= rooms.count()
    else :
        rooms = chatroom.objects.filter(room_type="public")
        b = rooms.count()
    return render(request , 'index.html' , {'room':rooms , 'username':username})
def register(request) :
    message = None
    try :
        tokens = request.COOKIES.get('access_token')
        if tokens :
            return redirect('main')
    except :
        pass
    if request.method == 'POST' :
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        hashed_password = PasswordGenerator.salt_hash_generator(password)
        hashed_password_str = hashed_password.decode('utf-8')
        try :
            sweetuser = Sweetusers(username=username , email=email , set_password=hashed_password_str)
            sweetuser.save()
            token = Myrefreshtoken.for_user(sweetuser)
            access_token  = str(token.access_token)
            refresh_token = str(token)
            response = redirect('main')
            response.set_cookie(
                'access_token', value=access_token,max_age=84600, httponly=True, secure=False, samesite='Strict'
            )
            response.set_cookie(
                'refresh_token', value=refresh_token,max_age=84600, httponly=True, secure=False, samesite='Strict'
            )
            return response
        except :
            message = "Username already taken pls choose another one"
    return render(request , 'register.html' , {'message':message})


def rooms(request , pk) :
    ct = chatroom.objects.get(id=pk)
    return render(request , 'password.html',{'cts':ct})

def createroom(request):
    try :
        tokens = request.COOKIES.get('access_token')
        response = PasswordGenerator.decode_token(tokens)
        user_id = response['id']
    except :
        return redirect('li')
    user = Sweetusers.objects.get(id=user_id)
    if request.method=='POST' :
        room_name = request.POST.get('room_name')
        bio = request.POST.get('bio')
        room_id  = PasswordGenerator.generate()
        room_type = request.POST.get('room_types')
        Room = chatroom(host=user,name=room_name,bio=bio,room_id=room_id,room_type=room_type)
        Room.save()
        return redirect('main')
    return render(request , 'from.html')
def Profile_page(request) :
    try :
        tokens = request.COOKIES.get('access_token')
        response = PasswordGenerator.decode_token(tokens)
        user_id = response['id']
    except :
        return redirect('li')
    if(user_id) :
        user_profile = Sweetusers.objects.get(id=user_id)
        try :
            rooms_created = chatroom.objects.filter(host=user_profile)
        except :
            rooms_created = None
        return render(request , 'profile.html' , {'user':user_profile,'rooms':rooms_created})
    else :
        return redirect('li')

def login_users(request) :
    login_msg = None
    if request.method == 'POST' :
        name = request.POST.get('us')
        password = request.POST.get('pa')
        print('password:',password)
        print(name)
        try :
            user = Sweetusers.objects.get(username=name)
            print(user.set_password)
        except :
            user = None
            login_msg = "Username doesnt exist"
        if user is not None :
            if PasswordGenerator.check_password(password.encode('utf-8') , user.set_password) :
                print("its alright your in........")
                token = Myrefreshtoken.for_user(user)
                access_token  = str(token.access_token)
                refresh_token = str(token)
                response = redirect('main')
                response.set_cookie(
                    'access_token', value=access_token,max_age=84600, httponly=True, secure=False, samesite='Strict'
                )
                response.set_cookie(
                    'refresh_token', value=refresh_token,max_age=84600, httponly=True, secure=False, samesite='Strict'
                )
                return response
            else :
                login_msg = "Password not matched try again.."
    return render(request , 'logge.html' , {"login_msg" : login_msg})
def getout(request) :
    response =  redirect('/')
    response.delete_cookie('id')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    response.delete_cookie('chat_id')
    request.session.flush()
    return response


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
            return redirect('main')
            print("room not found")
    return render(request , 'private_room_password.html')


def chatting(request,pk) :
    try :
        tokens = request.COOKIES.get('access_token')
        response = PasswordGenerator.decode_token(tokens)
        user_id = response['id']
    except :
        return redirect('li')
    if(user_id) :
        user = Sweetusers.objects.get(id=user_id)
        try :
            chat_room = chatroom.objects.get(id=pk)
            return render(request , 'chat.html' ,{'room': chat_room , 'user':user})
        except :
            return redirect('rooms',pk=pk)
    else :
        return redirect('li')


def delete_chatroom(request,pk) :
    room = chatroom.objects.get(id=pk)
    room.delete()
    return redirect('main')
