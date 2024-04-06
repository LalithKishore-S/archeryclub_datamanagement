
from django.urls import path
from .import views

urlpatterns = [
    path('coach_login',views.coach_login,name='coach_login'),
    path('enroll_your_champion',views.enroll_your_champion,name='enroll_your_champion'),
    path('sad_to_see_your_champion_go',views.sad_to_see_your_champion_go,name='sad_to_see_your_champion_go'),
    path('update_your_guy',views.update_your_guy,name='update_your_guy'),
    path('analyse_your_student',views.analyse_your_student,name='analyse_your_student'),
    path('achieving_excellence_through_matches',views.achieving_excellence_through_matches,name='achieving_excellence_through_matches'),
    path('match_details',views.match_details,name='match_details'),
    path('insert_fitness_test',views.insert_fitness_test,name='insert_fitness_test'),
    path('view_fitness_details',views.view_fitness_details,name='view_fitness_details'),
    path('modify_fitness_test',views.modify_fitness_test,name='modify_fitness_test'),
    path('modify_training_protocol',views.modify_training_protocol,name='modify_training_protocol'),
]