from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from .models import Hit,Conversation
import random
from .MyCommon import *
# Create your views here.
def index(request):
    rep = render(request, 'chatai/index.html')
    rep.set_cookie("login_room","-1")
    return rep

def register(request):
    cur_room = MyCommon.glb_room
    new_hit_id =sorted(cur_room)[0]
    MyCommon.glb_room.remove(new_hit_id)
    password = str(random.randint(0,10))+str(random.randint(0, 10))+str(random.randint(0, 10))+str(random.randint(0, 10))
    hit = Hit(hit_number=new_hit_id,security_code=password)
    print("ok1")
    scene = MyCommon.glb_scene[random.randint(0,len(MyCommon.glb_scene)-1)]
    emotion = MyCommon.glb_emotion[random.randint(0,len(MyCommon.glb_emotion)-1)]
    hit.save()
    print("ok2")
    conv = Conversation(scene=scene,emotion=emotion,hit=hit)
    conv.save()
    hit.current_conv = conv.pk
    hit.save()
    rep = render(request, 'chatai/register.html', {"new_hit_id": hit.hit_number, "password": hit.security_code})
    rep.set_cookie("login_room",str(new_hit_id),max_age=100)
    return rep

def login(request):
    return render(request,'chatai/login.html')