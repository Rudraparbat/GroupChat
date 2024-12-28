from django.contrib import admin
from django.urls import path , include
from conn import views

urlpatterns = [
    path('',views.home , name='home'),
    path('maine/', views.main,name='main'),
    path('rooms/<str:pk>/' , views.rooms , name='room'),
    path('chats/<str:pk>/' , views.chatting , name='ch'),
    path('crooms' , views.createroom , name='cr'),
    path('private_room' , views.private_room , name='private'),
    path('profile/',views.Profile_page,name='profile'),
    path('signup/' , views.register , name='si'),
    path('login/' , views.login_users , name='li'),
    path('logout/' , views.getout , name='go'),
]
