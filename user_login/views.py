from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

username=""
# Create your views here.
def archer_login(request):
    if request.method=='POST':
       username=request.POST['username']
       password=request.POST['password']
       user=auth.authenticate(username=username,password=password)
       if user is not None:
           auth.login(request,user)
           return redirect("/")
       else:
           messages.info(request,'invalid credentials')
           return redirect("archer_login")
    else:
       return render(request,"user_login.html")