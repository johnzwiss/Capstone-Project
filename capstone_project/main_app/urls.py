from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup_view, name="signup"),
    path('student/game/', views.game, name ="game"),
    path('student/welcome/<int:student_id>/', views.student_welcome, name="welcome"),
    path('teacher/classroom/', views.teacher_view, name='teacher_view'),
    path('teacher/classroom/<int:classroom_id>/' , views.classroom_show, name='classroom_show'),
    path('teacher/classroom/<int:classroom_id>/<int:student_id>/' , views.student_show , name='student_show'),
    path('teacher/classroom/<int:classroom_id>/<int:pk>/update' , views.StudentUpdate.as_view(), name='student_update'),
    path('teacher/classroom/<int:classroom_id>/create' , views.StudentCreate.as_view(), name='student_create'),
    path('teacher/classroom/create', views.ClassroomCreate.as_view(), name='classroom_create')
    
]