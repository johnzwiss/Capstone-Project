from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from .forms import LoginForm
from .models import Student, Classroom
from .lessons import multiplication_lesson
import time

# Create your views here.

# index view
def index(request):
    return render(request, 'index.html')

# login view
def login_view(request):
    # we can use the same view for multiple HTTP requests
    # this can be done with a simple if statement
    if request.method == 'POST':
        # handle post request
        # we want to authenticate the user with the username and pw
        form = LoginForm(request.POST)
        # validate the form data
        if form.is_valid():
            # get the username and pw and save them to variables
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            # here we use django's built in authenticate method
            user = authenticate(username = u, password = p)
            # if you found a user with matching credentials
            if user is not None:
                # if that user has not been disabled by admin
                if user.is_active and user.is_staff:
                    # use django's built in login function
                    login(request, user)
                    return HttpResponseRedirect('/teacher/classroom')
                elif user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/student/welcome/' + str(user.id))
                else:
                    print('the account has been disabled')
            else:
                print('the username or password is incorrect')
    else:
        # the request is a get, we render the login page
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

# logout view
def logout_view(request):
    # print('####### THIS IS THE REQUEST #######')
    # print(request.user)
    logout(request)
    return HttpResponseRedirect('/')

# signup view
def signup_view(request):
    # if the req is a post, then sign them up
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            g = Group.objects.get(name='teacher')
            g.user_set.add(user)
            user.is_staff= True
            user.save()
            login(request, user)
            return HttpResponseRedirect('/user/' + str(user.username))
    # if the req is a get, then show the form
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


# game view 
tic = None
n = 1
correct = 0
game_complete = False
counter = None


def game(request):
    current_user = request.user
    student = Student.objects.get(user_id = current_user.id)
    j = len(student.lessons_completed)
    if request.method == 'POST':
        global n
        global correct
        global game_complete
        global tic
        global counter
        num1 = multiplication_lesson[j][n]['num1']
        num2 = multiplication_lesson[j][n]['num2']
        num3 = multiplication_lesson[j][n - 1]['num2']
        problem_answer = str((num1 * num3))
        try:
            answer1 = (request.POST["answer"])
        except KeyError:
            answer1 = 0
        if answer1 == problem_answer:
            correct +=1
        n += 1
        print(n)
        if n > 12:
            game_complete = True
            toc = time.perf_counter()
            counter = round((toc - tic), 2)
            print(game_complete, toc)
            
    else:
        current_user = request.user
        student = Student.objects.get(user_id = current_user.id)
        j = len(student.lessons_completed)
        game_complete = False
        n = 1
        answer1 = 0
        correct = 0
        num1 = multiplication_lesson[j][0]['num1']
        num2 = multiplication_lesson[j][0]['num2']
        num3 = multiplication_lesson[j][0 - 1]['num2']
        problem_answer = str((num1 * num3))
        tic = time.perf_counter()
        print("THIS IS ON LOAD", num1, num2, tic)
    return render (request, 'student/game.html', {'multiplication_lesson' : multiplication_lesson, 'n': n, 'answer1' : answer1, 'num1': num1, 'num2': num2, 'problem_answer': problem_answer, 'correct': correct, 'game_complete': game_complete, 'counter': counter})



def student_welcome(request, student_id):
    current_user = request.user
    student = Student.objects.get(user_id = current_user.id)
    print(student.lessons_completed)
    return render(request, 'student/welcome.html', {'student': student})


# Teacher View
@user_passes_test(lambda user: user.is_staff)
def teacher_view(request):
    # get the current user 
    current_user = request.user
    
    # list all the classrooms that belong to current teacher
    classrooms = Classroom.objects.all().filter(user_id=current_user.id)
    return render (request, 'teacher/classroom.html', {'classrooms': classrooms})


# SELECT * FROM main_app_classroom JOIN main_app_student ON main_app_classroom.id = main_app_student.classroom_id;

# Teacher View classroom
@user_passes_test(lambda user: user.is_staff)
def classroom_show(request, classroom_id):

    # query to get the classroom based off url id
    classroom = Classroom.objects.get(id=classroom_id)
    # query to get the students from that classroom 
    students = Student.objects.filter(classroom_id = classroom_id)

    
    # render the classroom show view with the queried information
    return render (request, 'teacher/classroom_show.html', { 'classroom': classroom , 'students': students})
