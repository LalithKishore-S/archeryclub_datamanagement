
from django.urls import path
from .import views

urlpatterns = [
    path('archer_login',views.archer_login,name='archer_login'),
    path('practice_details_entry',views.practice_details_entry,name='practice_details_entry'),
    path('match_details_user',views.match_details_user,name='match_details_user'),
    path('practice_details',views.practice_details,name='practice_details'),
    path('training_protocol',views.training_protocol,name='training_protocol'),
    path('archer_portal',views.archer_portal,name='archer_portal'),
    path('profile',views.profile,name='profile'),
    path('modify_practice',views.modify_practice,name='modify_practice')
]