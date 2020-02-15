from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from .models import Hit,Conversation
import random
from .MyCommon import *
from .XmlFileCode import *
# Create your views here.
if not XmlCmd.isFileExist(MyCommon.glb_path):
    XmlCmd.createXml(MyCommon.glb_path)
    a=XmlCmd.writeXml(MyCommon.glb_path,["vacant_room","[6,7,8,9,10]"],"Hit","vacant_room")

def index(request):
    rep = render(request, 'chatai/index.html')
    rep.set_cookie("login_room", "5", max_age=60 * 60)
    rep.set_cookie("name", "siyang", max_age=60 * 60)
    return rep

def register(request):
    vacant_room = XmlCmd.readXml(MyCommon.glb_path,"Hit","vacant_room")[1]
    cur_room = eval(vacant_room)
    new_hit_id =sorted(cur_room)[0]
    cur_room.remove(new_hit_id)
    XmlCmd.writeXml(MyCommon.glb_path, ["vacant_room", "["+",".join([str(item) for item in cur_room])+"]"], "Hit", "vacant_room")
    password = str(random.randint(0,10))+str(random.randint(0, 10))+str(random.randint(0, 10))+str(random.randint(0, 10))
    scene = MyCommon.glb_scene[random.randint(0,len(MyCommon.glb_scene)-1)]
    emotion = MyCommon.glb_emotion[random.randint(0,len(MyCommon.glb_emotion)-1)]
    hit = Hit(hit_number=new_hit_id, security_code=password)
    hit.save()
    conv = Conversation(scene=scene, emotion=emotion, hit=hit)
    conv.save()
    hit.current_conv = conv.pk
    hit.save()
    rep = render(request, 'chatai/register.html', {"new_hit_id": hit.hit_number, "password": hit.security_code})
    rep.set_cookie("login_room",str(new_hit_id),max_age=60*60)
    return rep

def room(request,room_id):
    hit = get_object_or_404(Hit, hit_number=room_id)
    conv = get_object_or_404(Conversation,pk=hit.current_conv)
    name = request.COOKIES.get("name", None)
    if int(request.COOKIES.get("login_room",-1))==room_id:
        print("房间号正确")
        print(hit.speaker_name is None,hit.listener_name,conv.context is None,conv.utterances)
        if hit.speaker_name is None:
            rep = render(request, 'chatai/room.html', {"hit": hit, "conv": conv, "room_id": room_id, "name": name})
            print("speaker:",request.POST.get("speaker_name",False))
            if request.POST.get("speaker_name",False):
                print("修改speaker")
                hit.speaker_name = request.POST["speaker_name"]
                hit.save()
                rep = render(request, 'chatai/room.html', {"hit": hit, "conv": conv, "room_id": room_id, "name": name})
                rep.set_cookie("name", hit.speaker_name, max_age=60 * 60)
        elif hit.listener_name is None:
            print("保存listener_name")
            rep = render(request, 'chatai/room.html', {"hit": hit, "conv": conv, "room_id": room_id, "name": name})
            if request.POST.get("listener_name", False):
                print("保存listener_name",request.POST["listener_name"])
                hit.listener_name = request.POST["listener_name"]
                hit.save()
                rep = render(request, 'chatai/room.html', {"hit": hit, "conv": conv, "room_id": room_id, "name": name})
                rep.set_cookie("name", hit.listener_name, max_age=60 * 60)
        elif conv.context is None:
            if name==hit.speaker_name:
                print("进入阶段2：",request.POST.get("choice",False))
                if not request.POST.get("choice",False):
                    rep = render(request, 'chatai/room.html',{"hit":hit,"conv":conv,"room_id":room_id,"name":name,'error_message':"You didn't select a choice."})
                elif request.POST.get("choice",False)=="0":
                    print("context文本:",request.POST.get("context",False))
                    if request.POST.get("context",False):
                        conv.context = request.POST["context"]
                        conv.save()
                        rep = render(request, 'chatai/room.html',{"hit": hit, "conv": conv, "room_id": room_id, "name": name})
                    else:
                        rep = render(request, 'chatai/room.html',{"hit": hit, "conv": conv, "room_id": room_id, "name": name,'error_message': "你选择创造场景但没有输入文本"})
                elif request.POST.get("choice",False)=="1":
                    conv.scene = MyCommon.glb_scene[random.randint(0, len(MyCommon.glb_scene) - 1)]
                    conv.emotion = MyCommon.glb_emotion[random.randint(0, len(MyCommon.glb_emotion) - 1)]
                    conv.save()
                    rep = render(request, 'chatai/room.html', {"hit": hit, "conv": conv, "room_id": room_id, "name": name})
            else:
                print("打印",hit.listener_name is None ,hit.speaker_name,name)
                rep = render(request, 'chatai/room.html', {"hit": hit, "conv": conv, "room_id": room_id, "name": name})
        elif conv.utterances is None:
            rep = render(request, 'chatai/room.html', {"hit": hit, "conv": conv, "room_id": room_id, "name": name})
    else:
        rep = redirect(reverse("chatai:login",kwargs={"room_id":room_id}))
    return rep

def login(request,room_id):
    return render(request,'chatai/login.html',{"room_id":room_id})

def verify(request,room_id):
    hit = get_object_or_404(Hit, hit_number=room_id)
    if request.POST.get("password","") == hit.security_code:
        rep = redirect(reverse("chatai:room",kwargs={"room_id":room_id}))
        print("login_room",room_id)
        rep.set_cookie("login_room", str(room_id), max_age=60 * 60)
        print("name",request.POST.get("name", ""))
        rep.set_cookie("name", request.POST.get("name", ""), max_age=60 * 60)
    else:
        rep = redirect(reverse("chatai:login",kwargs={"room_id":room_id}))
    return rep


