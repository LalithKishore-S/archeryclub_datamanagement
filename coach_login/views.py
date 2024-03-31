from django.shortcuts import render

# Create your views here.
def coach_login(request):
    return render(request,"coach_login.html")