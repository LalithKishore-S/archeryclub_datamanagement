from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.db import connections,transaction

# Create your views here.
def coach_login(request):
    if request.method=='POST':
       username=request.POST['username']
       password=request.POST['password']
       user=auth.authenticate(username=username,password=password)
       if user is not None and user.is_superuser:
           auth.login(request,user)
           return render(request,"coach_portal.html")
       else:
           messages.info(request,'invalid credentials')
           return redirect("coach_login")
    else:
       return render(request,"coach_login.html")
   
def enroll_your_champion(request):
    if request.method=="POST":
        aid=request.POST['AID']
        gender=request.POST['gender']
        category=request.POST['category']
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT AID FROM PLAYER")
            data=cursor.fetchall()
            print(data)
        if aid in [item[0] for item in data]:
            messages.info(request,'AID already exists')
            return redirect("enroll_your_champion")
        elif aid[0]!='A' and  aid[0]!='a':
            messages.info(request,'AID format wrong....Expected ex:A01')
            return redirect("enroll_your_champion")
        elif category not in ('recurve','compound','indian'):
            messages.info(request,'Invalid Category...Must be within recurve,compound or indian')
            return redirect("enroll_your_champion")
        elif gender not in ('m','f','t') and gender not in ('M','F','T'):
            messages.info(request,'Invalid Gender')
            return redirect("enroll_your_champion")
        else:
            name=request.POST['name']
            dob=request.POST['dob']
            phno=request.POST['phno']
            addr=request.POST['add']
            with connections['default'].cursor() as cursor:
                cursor.execute("INSERT INTO PLAYER VALUES(INITCAP(:aid),:name,TO_DATE(:dob,'DD-MM-YYYY'),UPPER(:gender),:phno,:addr,:category)",{'aid':aid,'name':name,'dob':dob,'gender':gender,'phno':phno,'addr':addr,'category':category})
        return redirect("coach_portal")
    else:
        return render(request,"enroll-your-champion.html")

def sad_to_see_your_champion_go(request):
    if request.method=='POST':
        aid=request.POST['AID']
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT AID FROM PLAYER")
            data=cursor.fetchall()
            print(data)
        if aid not in [item[0] for item in data]:
            messages.info(request,'AID does not exist')
            return redirect("sad_to_see_your_champion_go")
        elif aid[0]!='A' and  aid[0]!='a':
            messages.info(request,'AID format wrong....Expected ex:A01')
            return redirect("sad_to_see_your_champion_go")
        else:
            with connections['default'].cursor() as cursor:
                cursor.execute("DELETE FROM PLAYER WHERE AID=:AID",{'AID':aid})
        return redirect("coach_portal")
    else:
        return render(request,"sad-to-see-your-chanpion-go.html")

def update_your_guy(request):
    if request.method=="POST":
        aid=request.POST['AID']
        gender=request.POST['gender']
        category=request.POST['category']
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT AID FROM PLAYER")
            data=cursor.fetchall()
        existing_aids=[item[0] for item in data]
        if aid not in existing_aids:
            messages.info(request,'AID does not exist')
            return redirect("update_your_guy")
        elif aid[0]!='A' and  aid[0]!='a':
            messages.info(request,'AID format wrong....Expected ex:A01')
            return redirect("update_your_guy")
        elif category not in ('recurve','compound','indian'):
            messages.info(request,'Invalid Category...Must be within recurve,compound or indian')
            return redirect("update_your_guy")
        elif gender not in ('m','f','t') and gender not in ('M','F','T'):
            messages.info(request,'Invalid Gender')
            return redirect("update_your_guy")
        else:
            name=request.POST['name']
            dob=request.POST['dob']
            phno=request.POST['phno']
            addr=request.POST['add']
            with connections['default'].cursor() as cursor:
                cursor.execute("UPDATE PLAYER SET NAME=:name,DOB=TO_DATE(:dob,'DD-MM-YYYY'),GENDER=:gender,PHONENO=:phno,ADDRESS=:addr,CATEGORY=:category WHERE AID=:aid",{'aid':aid,'name':name,'dob':dob,'gender':gender,'phno':phno,'addr':addr,'category':category})
        return redirect("coach_portal")
    else:
        return render(request,"update-your-guy.html")

def analyse_your_student(request):
    with connections['default'].cursor() as cursor:
            cursor.execute("SELECT * FROM PLAYER")
            data=cursor.fetchall()
    return render(request,"analyse-your-student.html",{'data':data})

def achieving_excellence_through_matches(request):
    if request.method=='POST':
        match_name=request.POST['name']
        dom=request.POST['dom']
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT MATCH_NAME FROM MATCH")
            data=cursor.fetchall()
        existing_matches=[item[0] for item in data]
        if match_name in existing_matches:
            messages.info(request,'match detail already exists')
            return redirect("achieving_excellence_through_matches")
        else:
            with connections['default'].cursor() as cursor:
                cursor.execute("INSERT INTO MATCH VALUES(:match_name,to_date(:dom,'DD-MM-YYYY'))",{'match_name':match_name,'dom':dom})
        return redirect("coach_portal")
    else:
        return render(request,"achieving-excellence-through-matches.html")

def match_details(request):
    if request.method=='POST':
        aid=request.POST['aid']
        match_name=request.POST['match_name']
        existing_aids=[]
        existing_matches=[]
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT MATCH_NAME FROM MATCH")
            data=cursor.fetchall()
            existing_matches=[item[0] for item in data]
            cursor.execute("SELECT AID FROM PLAYER")
            data=cursor.fetchall()
            existing_aids=[item[0] for item in data]
        if match_name not in existing_matches:
            messages.info(request,'The given match name does not exist')
            return redirect("match_details")
        elif aid not in existing_aids:
            messages.info(request,'AID does not exist')
            return redirect("match_details")
        else:
            data=None
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT AID,MATCH_NAME FROM ATTENDS WHERE AID=:aid AND MATCH_NAME=:match",{'aid':aid,'match':match_name})
                data=cursor.fetchall()
            if not data:
                agg_score=int(request.POST['agg_score'])
                scale=int(request.POST['scale'])
                if agg_score>scale or scale%360!=0:
                    messages.info(request,'Pls check the scores and scales')
                    return redirect("match_details")
                else:
                    rank=request.POST['rank']
                    with connections['default'].cursor() as cursor:
                        cursor.execute("INSERT INTO ATTENDS VALUES(:aid,:match,:agg,:scale,:rank)",{'aid':aid,'match':match_name,'agg':agg_score,'scale':scale,'rank':rank})
                return redirect(coach_portal)
            else:
                messages.info(request,'The details of the player for the given match already exists')
                return redirect("match_details")
    else:
        return render(request,"match-details.html")

def insert_modify_fitness_test(request):
    if request.method=='POST':
        aid=request.POST['AID']
        existing_aids=[]
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT AID FROM PLAYER")
            data=cursor.fetchall()
            existing_aids=[item[0] for item in data]
            cursor.close()
        if aid not in existing_aids:
            messages.info(request,'AID does not exist')
            return redirect("insert_modify_fitness_test")
        else:
            existing_aids=[]
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT AID FROM FITNESSTEST")
                data=cursor.fetchall()
                print(data)
                existing_aids=[item[0] for item in data]
                cursor.close()
            if aid in existing_aids:
                with connections['default'].cursor() as cursor:
                    cursor.execute("DELETE FROM FITNESSTEST WHERE AID=:AID",{'AID':aid})
                    cursor.close()
            nos=int(request.POST['nos'])
            nob=int(request.POST['nob'])
            time=float(request.POST['time'])
            if nos>40 and nob>=10 and time<=16:
                res='P'
            elif nob<5 and time>20:
                res='B'
            else:
                res='I'
            with connections['default'].cursor() as cursor:
                cursor.execute("INSERT INTO FITNESSTEST VALUES(:AID,:NOS,:NOB,:TIME,:RES)",{'AID':aid,'NOS':nos,'NOB':nob,'TIME':time,'RES':res})
        return redirect("coach_portal")
    else:
        return render(request,"insert-fitness-test.html")

def view_fitness_details(request):
    with connections['default'].cursor() as cursor:
            cursor.execute("SELECT A.NAME,B.* FROM FITNESSTEST B INNER JOIN PLAYER A ON A.AID=B.AID")
            data=cursor.fetchall()
    return render(request,"view-fitness-details.html",{'data':data})

def view_match_practice(request):
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT AID,NAME,MATCH_NAME,DOM,AGG_SCORE,OUT_OF,RANK FROM ATTENDS NATURAL JOIN MATCH NATURAL JOIN PLAYER ")
        data1=cursor.fetchall()
        cursor.execute("SELECT AID,NAME,DOP,DISTANCE,NO_ARROWS,AGG_SCORE,OUT_OF FROM PRACTICE NATURAL JOIN PLAYER")
        data2=cursor.fetchall()
    return render(request,"coach_portal_view_match_practice.html",{'data1':data1,'data2':data2})

def modify_training_protocol(request):  
    if request.method=='POST':
        res=request.POST['res']
        if res in ('P','I','B'):
            with connections['default'].cursor() as cursor:
                cursor.execute("UPDATE TRAINPROT SET MON=:M,TUES=:T,WED=:W,THURS=:TH,FRI=:F,SAT=:S,SUN=:SU WHERE RESULT=:R",{'R':res,'M':request.POST['mon'],'t':request.POST['tues'],'w':request.POST['wed'],'th':request.POST['thurs'],'f':request.POST['fri'],'s':request.POST['sat'],'su':request.POST['sun'],})
            return redirect("coach_portal")
        else:
            messages.info(request,"Result type must be in (P,I,B)")
            return redirect("modify_training_protocol")
    else:
        return render(request,"modify-training-protocol.html")

def coach_portal(request):
    return render(request,"coach_portal.html")