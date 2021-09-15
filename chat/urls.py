from django.urls import path

from . import views


app_name='chat'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.login, name='login'),
    path('chatting/',views.chatting, name='chatting'),
    path('sending/',views.sending, name='sending'),
   ]
