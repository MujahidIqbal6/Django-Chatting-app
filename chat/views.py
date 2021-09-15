from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from .models import User,Mesg



# Create your views here.

def index(request):
    '''
    view func for main index page
    '''
    #load html template
    template = loader.get_template('chat/index.html')
    #empty context
    context = {}
    return HttpResponse(template.render(context, request))


def chatting(request):
    #list to maintain all signed in users
    users_active=[]

    #saving all users to active user list
    for key in request.session.keys():
        if "#user_" in key:
            users_active.append(key[6:])
   
 
    user1_msgs=User.objects.get(user_name=request.session['user1']).mesg_set.all()
    user2_msgs=User.objects.get(user_name=request.session['user2']).mesg_set.all()
         
    template = loader.get_template('chat/chatting.html')
    context = {'users':users_active, 'user1':request.session['user1'],'user2':'Sohaib','user1_msgs':user1_msgs,'user2_msgs':user2_msgs}
    return HttpResponse(template.render(context, request))

def sending(request):
    '''
    view func for receiving new text message
    '''
    if request.POST:
        #get current msg
        msg = request.POST['newmsg']
        user=User.objects.get(user_name=request.session['user1'])
        new_msg=Mesg(msg_text=msg,user=user)
        new_msg.save()
    return HttpResponseRedirect(reverse('chat:chatting', args=()))

def login(request):
    '''
    view func for logging current user using username and pass
    '''
    #if its a post request from client
    if request.POST:
        #reading username and password from request object
        username = request.POST['Uname']
        password = request.POST['Pass']

        #get current user from DB
        current_user=User.objects.filter(user_name=username,password=password).count()

        #if correct credentials
        if current_user==1:
            #save current user to session object
            request.session["#user_"+username]=1
            request.session['user1']=username
            request.session['user2']='sohaib'
            request.session.modified = True
            return HttpResponseRedirect(reverse('chat:chatting', args=()))

        else:
            #redirect to main index page with error shown
            template = loader.get_template('chat/index.html')
            context = {'error':'1'}
            return HttpResponse(template.render(context, request))

    



