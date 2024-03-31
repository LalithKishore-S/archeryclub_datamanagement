
from django.urls import path
from .import views

urlpatterns = [
    path('archer_login',views.archer_login,name='archer_login'),
]