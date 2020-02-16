from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from .models import Hit,Conversation,Utterance
import random
from .MyCommon import *
from .XmlFileCode import *
# Create your views here.
if not XmlCmd.isFileExist(MyCommon.glb_path):
    XmlCmd.createXml(MyCommon.glb_path)
    a=XmlCmd.writeXml(MyCommon.glb_path,["vacant_room","[1,2,3,4,5,6,7,8,9,10]"],"Hit","vacant_room")

def index(request):
    rep = render(request, 'chatai/index.html')
    if request.POST.get("room_id",False) and request.POST.get("room_id",False).isdigit():
        room_id = int(request.POST["room_id"])
        if room_id >0:
            rep = redirect(reverse("chatai:login",kwargs={"room_id":room_id}))
    return rep

def register(request):
    if not XmlCmd.isFileExist(MyCommon.glb_path):
        XmlCmd.createXml(MyCommon.glb_path)
        XmlCmd.writeXml(MyCommon.glb_path, ["vacant_room", "[1,2,3,4,5,6,7,8,9,10]"], "Hit", "vacant_room")
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
        elif hit.listener_name is None:
            print("保存listener_name")
            rep = render(request, 'chatai/room.html', {"hit": hit, "conv": conv, "room_id": room_id, "name": name})
            if request.POST.get("listener_name", False):
                print("保存listener_name",request.POST["listener_name"])
                hit.listener_name = request.POST["listener_name"]
                hit.save()
                rep = render(request, 'chatai/room.html', {"hit": hit, "conv": conv, "room_id": room_id, "name": name})
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
                        rep = render(request, 'chatai/room.html',{"hit": hit, "conv": conv, "room_id": room_id, "name": name,"cur_turn":0})
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
        elif name in [hit.speaker_name,hit.listener_name]:
            if conv.utterances.count()==0:
                cur_turn = 0
            else:
                cur_turn = int(1-conv.utterances.latest("send_time").speaker_idx)
            if request.POST.get("speaker_text",False) and cur_turn==0:
                u = Utterance(text=request.POST["speaker_text"],speaker_idx=0)
                u.save()
                conv.utterances.add(u)
                conv.save()
                rep = render(request, 'chatai/room.html', {"hit": hit, "conv": conv, "room_id": room_id, "name": name,"history":conv.utterances.order_by("send_time"),"cur_turn":int(1-cur_turn),"length":conv.utterances.count()})
            elif request.POST.get("listener_text",False) and  cur_turn==1:
                u = Utterance(text=request.POST["listener_text"],speaker_idx=1)
                u.save()
                conv.utterances.add(u)
                conv.save()
                rep = render(request, 'chatai/room.html', {"hit": hit, "conv": conv, "room_id": room_id, "name": name,"history":conv.utterances.order_by("send_time"),"cur_turn":int(1-cur_turn),"length":conv.utterances.count()})
            else:
                rep = render(request, 'chatai/room.html', {"hit": hit, "conv": conv, "room_id": room_id, "name": name,"history":conv.utterances.order_by("send_time"),"cur_turn":cur_turn,"length":conv.utterances.count()})
        else:
            rep = redirect(reverse("chatai:login", kwargs={"room_id": room_id}))
    else:
        rep = redirect(reverse("chatai:login",kwargs={"room_id":room_id}))
    rep.set_cookie("name", name, max_age=60 * 60)
    rep.set_cookie("login_room", room_id, max_age=60 * 60)
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
def close(request,room_id):
    print("hehes",request.POST.get("close",False),"haha")
    hit = get_object_or_404(Hit, hit_number=room_id)
    name = request.COOKIES.get("name",None)
    if request.POST.get("close", False)=="1" and hit.speaker_name==name:
        conv = get_object_or_404(Conversation,pk=hit.current_conv)
        conv.hit=None
        conv.save()
        hit.delete()
        vacant_room = XmlCmd.readXml(MyCommon.glb_path, "Hit", "vacant_room")[1]
        cur_room = eval(vacant_room)
        cur_room = list(set(cur_room + [room_id]))
        XmlCmd.writeXml(MyCommon.glb_path, ["vacant_room", "[" + ",".join([str(item) for item in cur_room]) + "]"],
                        "Hit", "vacant_room")

        return render(request,"chatai/close.html",{"result":"对话结束，链接已收回！"})
    else:
        return render(request, "chatai/close.html", {"result": "无权限收回对话。如果您觉得有权限，可重新登录试试。"})



