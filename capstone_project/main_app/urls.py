from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup_view, name="signup"),
    path('student/game', views.game, name ="game"),
    path('teacher/classroom', views.teacher_view, name='teacher_view')
    
]