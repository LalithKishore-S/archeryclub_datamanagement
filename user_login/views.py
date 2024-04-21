from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.db import connections
from datetime import datetime

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
    with connections['default'].cursor() as cursor:
            username=request.user.username
            cursor.execute("SELECT AID FROM PLAYER WHERE NAME=:username",{'username':username})
            aid=cursor.fetchone()[0]
            cursor.execute("SELECT MATCH_NAME,DOM,AGG_SCORE,OUT_OF,RANK FROM ATTENDS NATURAL JOIN MATCH NATURAL JOIN PLAYER WHERE AID=:AID",{'AID':aid})
            data=cursor.fetchall()
            formatted_data=[]
            for row in data:
                dop_str = row[1]  
                formatted_dop = dop_str.strftime("%B %d, %Y")  
                formatted_row = (row[0],)+(formatted_dop,) +row[2:]  
                formatted_data.append(formatted_row)
    return render(request,"boast-yourself.html",{'data':formatted_data})

def practice_details(request):
    with connections['default'].cursor() as cursor:
            username=request.user.username
            cursor.execute("SELECT AID FROM PLAYER WHERE NAME=:username",{'username':username})
            aid=cursor.fetchone()[0]
            cursor.execute("SELECT DOP,DISTANCE,NO_ARROWS,AGG_SCORE,OUT_OF FROM PRACTICE NATURAL JOIN PLAYER WHERE AID=:AID",{'AID':aid})
            data=cursor.fetchall()
            formatted_data = []
            for row in data:
                dop_str = row[0]  
                formatted_dop = dop_str.strftime("%B %d, %Y")  
                formatted_row = (formatted_dop,) + row[1:] 
                formatted_data.append(formatted_row)
    return render(request,"know-how-well-you-have-performed.html",{'data':formatted_data})

def training_protocol(request):
    with connections['default'].cursor() as cursor:
            username=request.user.username
            cursor.execute("SELECT AID FROM PLAYER WHERE NAME=:username",{'username':username})
            aid=cursor.fetchone()[0]
            cursor.execute("SELECT RESULT,MON,TUES,WED,THURS,FRI,SAT,SUN FROM FITNESSTEST NATURAL JOIN TRAINPROT NATURAL JOIN PLAYER WHERE AID=:AID",{'AID':aid})
            data=cursor.fetchall()
    return render(request,"know-about-yourself.html",{'data':data})

def profile(request):
    with connections['default'].cursor() as cursor:
            username=request.user.username
            cursor.execute("SELECT AID FROM PLAYER WHERE NAME=:username",{'username':username})
            aid=cursor.fetchone()[0]
            cursor.execute("SELECT * FROM PLAYER WHERE AID=:AID",{'AID':aid})
            data=cursor.fetchall()
            formatted_data=[]
            for row in data:
                dop_str = row[2]  
                formatted_dop = dop_str.strftime("%B %d, %Y")  
                formatted_row = row[0:2]+(formatted_dop,) +row[3:]  
                formatted_data.append(formatted_row)
    return render(request,"profile.html",{'data':formatted_data})

def modify_practice(request):
    if request.method=='POST':
        dop=request.POST['dop']
        date_to_check = datetime.strptime(dop, "%d-%b-%Y")
        print(dop)
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
            cursor.execute("SELECT AID,DOP FROM PRACTICE WHERE AID=:aid",{'aid':aid})
            poss_pairs=cursor.fetchall()
            existing_details=[(item[0],item[1]) for item in poss_pairs]
            print(existing_details)
            if (aid,date_to_check) in existing_details:
                print("Successfull")
                cursor.execute("UPDATE PRACTICE SET DISTANCE=:dist,VOLUME_FLAG=:v_flag,NO_ARROWS=:no_arrows,SCORING_FLAG=:s_flag,AGG_SCORE=:score,OUT_OF=:scale WHERE AID=:aid AND DOP=to_date(:dop,'DD-MM-YYYY')",{'aid':aid,'dop':dop,'dist':dist,'v_flag':v_flag,'no_arrows':no_arrows,'s_flag':s_flag,'score':score,'scale':out_of})
                return redirect("archer_portal")   
            else:
                messages.info(request,'Practice details does not exist,so first insert it')
                return redirect("modify_practice")
    else:
        return render(request,"modify_practice.html")
