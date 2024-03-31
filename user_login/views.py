from django.shortcuts import render

# Create your views here.
def archer_login(request):
    return render(request,"user_login.html")