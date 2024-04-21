from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

def archer_registration(request):
    if request.method=='POST':
        first_name=request.POST['firstName']
        last_name=request.POST['secondName']
        phno=request.POST['phoneNo']
        email=request.POST['email']
        password=request.POST['password']
        
        if User.objects.filter(username=first_name).exists():
            messages.info(request,'Username Taken')
            return redirect('archer_registration')
        else:
            user=User.objects.create_user(username=first_name,password=password,email=email,first_name=first_name,last_name=last_name)
            user.save()
            return redirect('/')
    else:        
       return render(request,"user_registration.html")
