
from django.urls import path
from .import views

urlpatterns = [
    path('coach_login',views.coach_login,name='coach_login'),
]