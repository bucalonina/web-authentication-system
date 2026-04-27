#* Marko Dasic 2022/0731
#* Pavle Kotlajic 2021/0596

from django.contrib import admin
from django.urls import path, include
from . import views

from Aplikacija.views import *

urlpatterns = [
    path('home/', views.homePage, name='home'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('profile_user/<str:pk>/', views.profile_userPage, name='profile_user'),
    path('add_rating/<str:user_id>/', views.add_rating, name='add_rating'),
    path('update_user/', views.update_userPage, name='update_user'),
    path('profile_admin/', views.profile_adminPage, name='profile_admin'),
    path('main/', views.mainPage, name='main'),
    path('chats/', views.chatsPage, name='chats'),
    path('admin_ban/<str:user_id>/', views.admin_banPage, name='admin_ban'),
    path('delete/', views.deletePage, name='delete'),
    path('payment/', views.paymentPage, name='payment'),
    path('edit_profile/', views.edit_profilePage, name='edit_profile'),
    path('report/<str:pk>/', views.reportPage, name='report'),
    path('chat/<str:pk>/', views.chatPage, name='chat'),
    path('invite/', views.invitePage, name='invite'),
    path('delete_user/<str:user_id>/', views.delete_user, name='delete_user'),
    path('update_premium_flag/', update_premium_flag, name='update_premium_flag'),
    path('getreports/', views.getreports, name='getreports'),
    path('ban_user/<str:user_id>/', views.ban_user, name='ban_user'),
    path('edit_profile/', views.update_userPage, name='update_user'),
    path('send_message/', views.send_message, name='send_message'),
    path('submit_rating/', submit_rating, name='submit_rating'),
     
     
]
