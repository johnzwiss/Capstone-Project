from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic.base import RedirectView
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup_view, name="signup"),
    path('student/game/', views.game, name ="game"),
    path('student/welcome/<int:student_id>/', views.student_welcome, name="welcome"),
    path('student/results/', views.student_results, name="student_results"),
    path('teacher/classroom/', views.teacher_view, name='teacher_view'),
    path('teacher/classroom/<int:classroom_id>/' , views.classroom_show, name='classroom_show'),
    path('teacher/classroom/<int:classroom_id>/<int:student_id>/' , views.student_show , name='student_show'),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
   
        
]