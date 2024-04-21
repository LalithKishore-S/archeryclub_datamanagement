
from django.urls import path
from .import views

urlpatterns = [
    path('archer_registration',views.archer_registration,name='archer_registration'),
]