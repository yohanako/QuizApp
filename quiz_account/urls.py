from django.urls import path
from . import views

urlpatterns = [
path('login/', views.login_user, name= 'login'),
path('', views.home, name="home"),
path('logout/', views.logout_user, name= 'logout'),
path('register/', views.register_user, name= 'register'),
path('edit_profile/', views.edit_profile, name= 'edit_profile'),
path('change_password/', views.change_password, name= 'change_password'),


#Teacher URL's

path('teacher_login/',views.teacher_login, name='teacher_login'),
path('teacher_register/',views.teacher_register, name='teacher_register'),
path('teacher_logout/', views.teacher_logout, name= 'teacher_logout'),
path('teacher_create/',views.teacher_create, name='teacher_create'),
path('teacher_base/',views.teacher_base, name='teacher_base'),
path('teacher_signup/',views.teacher_signup, name='teacher_signup'),
path('teacher_click/',views.teacher_click, name='teacher_click'),
path('teacher_create_view/',views.teacher_create_view, name='teacher_create_view'),
path('teacher_create_topic/',views.teacher_create_topic, name='teacher_create_topic'),
path('teacher_see_topic/',views.teacher_see_topic, name='teacher_see_topic'),
path('teacher_topic/',views.teacher_topic, name='teacher_topic'),
path('teacher_create_question/',views.teacher_create_question, name='teacher_create_question'),
#path('teacher_see_question/',views.teacher_see_question, name='teacher_see_question'),
path('teacher_see_question/<int:pk>', views.teacher_see_question,name='teacher_see_question'),


#Student Url's

path('student_signup/',views.student_signup, name='student_signup'),
path('student/',views.student, name='student'),
#path('start_quiz/',views.start_quiz, name='start_quiz'),
#path('take_quiz/',views.take_quiz, name='take_quiz'),
path('student_quiz/',views.student_quiz, name='student_quiz'),
path('take_quiz/<int:pk>',views.take_quiz, name='take_quiz'),
path('start_quiz/<int:pk>',views.start_quiz,name='start_quiz'),


path('check_score/<int:pk>',views.check_score, name='check_score'),
path('see_score/',views.see_score, name='see_score'),
path('student_score/',views.student_score, name='student_score'),
path('calculate_marks/',views.calculate_marks, name='calculate_marks'),


]