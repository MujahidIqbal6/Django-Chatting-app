from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from .models import User,Mesg
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def index(request):
  
    '''
    view func for main index page
    '''
    #remove all temporary session data
    request.session.flush()
    #load html template
    template = loader.get_template('chat/index.html')
    #empty context
    context = {}
    #render html template and return response
    return HttpResponse(template.render(context, request))

@csrf_exempt
def setuser(request):
     '''
     post api to change second user
     '''
     if request.POST:
       #set second user value in session to clicked user value  
       request.session['user2']=request.POST['user']   
       #redirect to chatting page
       return HttpResponseRedirect(reverse('chat:chatting', args=()))

 


def chatting(request):
    '''
     view func to display main chatting page
    '''
    #list to maintain all signed in users
    users_active=[]

    #get all active users from DB
    for user in User.objects.filter(active=True):
        users_active.append(user.user_name)
    
    #get both users msgs
    user1_msgs=[]
    user2_msgs=[]

    #get user objects
    user1=User.objects.get(user_name=request.session['user1'])
    user2=User.objects.get(user_name=request.session['user2'])
    

    #check if user a selected a second user to chat or not
    if request.session['user2']!=request.session['user1']:

     #get msgs sent by user1 to user2   
     for msg in Mesg.objects.filter(from_user=user1,to_user=user2):
        user1_msgs.append(msg.msg_text)

     #get msgs sent by user2 to user1   
     for msg in Mesg.objects.filter(from_user=user2,to_user=user1):
        user2_msgs.append(msg.msg_text)

    #render and return html template     
    template = loader.get_template('chat/chatting.html')
    context = {'users':users_active, 'user1':request.session['user1'].upper(),'user2':request.session['user2'].upper(),'user1_msgs':user1_msgs,'user2_msgs':user2_msgs}
    return HttpResponse(template.render(context, request))

def sending(request):
    '''
    view func for receiving new text message
    '''
    if request.POST:
        #get current msg
        msg = request.POST['newmsg']
        user=User.objects.get(user_name=request.session['user1'])
        user2=User.objects.get(user_name=request.session['user2'])
        new_msg=Mesg(msg_text=msg,from_user=user,to_user=user2)
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
            request.session['user1']=username
            request.session['user2']=username
            request.session.modified = True

            #add user to online users
            u=User.objects.get(user_name=username,password=password)
            u.active=True
            u.save()
            
            #redirect to chatting page
            return HttpResponseRedirect(reverse('chat:chatting', args=()))

        else:
            #redirect to main index page with error shown
            template = loader.get_template('chat/index.html')
            context = {'error':'1'}
            return HttpResponse(template.render(context, request))

    



