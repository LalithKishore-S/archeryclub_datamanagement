from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.db import connections


# Create your views here.
def archer_login(request):
    if request.method=='POST':
       username=request.POST['username']
       password=request.POST['password']
       user=auth.authenticate(username=username,password=password)
       if user is not None:
           auth.login(request,user)
           return render(request,"archer-portal.html")
       else:
           messages.info(request,'invalid credentials')
           return redirect("archer_login")
    else:
       return render(request,"user_login.html")
   
def archer_portal(request):
    return render(request,"archer-portal.html")
   
def practice_details_entry(request):
    if request.method=='POST':
        dop=request.POST['dop']
        dist=int(request.POST['dist'])
        no_arrows=int(request.POST['no_arrows'])
        score=int(request.POST['score'])
        out_of=int(request.POST['scale'])
        v_flag=0
        s_flag=0
        aid=""
        if score==0 and out_of==0:
            s_flag=0
        elif no_arrows==0:
            v_flag=0
        username=request.user.username
        with connections['default'].cursor() as cursor:
            username=request.user.username
            cursor.execute("SELECT AID FROM PLAYER WHERE NAME=:username",{'username':username})
            aid=cursor.fetchone()[0]
            cursor.execute("INSERT INTO PRACTICE VALUES(:aid,to_date(:dop,'DD-MM-YYYY'),:dist,:v_flag,:no_arrows,:s_flag,:score,:scale)",{'aid':aid,'dop':dop,'dist':dist,'v_flag':v_flag,'no_arrows':no_arrows,'s_flag':s_flag,'score':score,'scale':out_of})
            return redirect("archer_portal")   
    else:
        return render(request,"user-enter-practicedet.html")

def match_details_user(request):
    return render(request,"boast-yourself.html")

def practice_details(request):
    return render(request,"know-how-well-you-have-performed.html")

def training_protocol(request):
    return render(request,"know-about-yourself.html")