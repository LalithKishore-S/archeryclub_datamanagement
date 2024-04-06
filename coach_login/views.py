from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages


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
    return render(request,"enroll-your-champion.html")

def sad_to_see_your_champion_go(request):
    return render(request,"sad-to-see-your-chanpion-go.html")

def update_your_guy(request):
    return render(request,"update-your-guy.html")

def analyse_your_student(request):
    return render(request,"analyse-your-student.html")

def achieving_excellence_through_matches(request):
    return render(request,"achieving-excellence-through-matches.html")

def match_details(request):
    return render(request,"match-details.html")

def insert_fitness_test(request):
    return render(request,"insert-fitness-test.html")

def view_fitness_details(request):
    return render(request,"view-fitness-details.html")

def modify_fitness_test(request):
    return render(request,"modify-fitness-test.html")

def modify_training_protocol(request):
    return render(request,"modify-training-protocol.html")