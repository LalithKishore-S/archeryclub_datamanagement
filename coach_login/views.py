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
           return redirect("/")
       else:
           messages.info(request,'invalid credentials')
           return redirect("coach_login")
    else:
       return render(request,"coach_login.html")