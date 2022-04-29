from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.forms import ModelChoiceField, IntegerField, MultipleChoiceField
from .forms import LoginForm
from .models import Student, Classroom
from .lessons import multiplication_lesson, animal, sound
from django import forms
import time, array, random



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
                # if user isn't staff then they are directed to the student page
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
            return HttpResponseRedirect('/teacher/classroom/')
    # if the req is a get, then show the form
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


# game view 
tic = None
n = 1
correct = 0
game_complete = False
lesson_pass = False
counter = None
j=0


def game(request):
    global j
    global n
    global correct
    global game_complete
    global tic
    global counter
    global lesson_pass
    ## find current user 
    current_user = request.user
    ## call student object 
    student = Student.objects.get(user_id = current_user.id)
    ## set iterator to length of lessons completed by current student
    j= len(student.lessons_completed)
    ## if all lessons are completed set students lesson back to 2nd lesson
    if j < 12:
        j = len(student.lessons_completed)
        print("this if statement is hittin", j)
    else:
        j= 1
    ## set animal picture based on which lesson is being done 
    animal_pic = animal[j]
    animal_sound = sound[j]
    print(animal_sound)
    ## this happens when a student enters an answer
    if request.method == 'POST':
    ## array of class names for positioning/moving animal 
        letter = ["a","b","c","d","e","f","g","h","i","j","k","l","l"]
    ## presenting the numbers a student needs to multiply and checking the answer
        num1 = multiplication_lesson[j][n]['num1']
        num2 = multiplication_lesson[j][n]['num2']
        num3 = multiplication_lesson[j][n - 1]['num2']
        problem_answer = str((num1 * num3))
        try:
            answer1 = (request.POST["answer"])
        except KeyError:
            answer1 = 0
    ## if answer is correct counter adds one
        if answer1 == problem_answer:
            correct +=1
    ## if answer is correct animal picture advances one stone
        picture = letter[correct]
    ## increase counter to progress to next question
        n += 1
    ## if student student has answered 12 questions and got 10 correct end the game 
        if n > 12 and correct > 10:
            game_complete = True
            lesson_pass = True
    ## stop timer
            toc = time.perf_counter()
    ## calculate time
            counter = str(round((toc - tic), 2))
    ## update lesson tracker 
            tracker = (len(student.lessons_completed) + 1)
    ## calculate score and give a percentage 
            score = str(round(correct/12 * 100, 2))
    ## update student model 
            student.lessons_completed.append(tracker)
            student.results.append('Score: ' + score + '%' ' Time: ' + counter)
            student.save()
    ## if student finishes game but doesn't pass
        elif n > 12 and correct <= 10:
            game_complete = True
            lesson_pass = False
    ## stop timer
            toc = time.perf_counter()
    ## calculate time 
            counter = str(round((toc - tic), 2))
    ## update lesson tracker 
            tracker = (len(student.lessons_completed) + 1)
    ## caluclate score in percentage 
            score = str(round(correct/12 * 100, 2))
    ## if students hasn't attemped any lessons, append lessons attempted 
            if len(student.lessons_attempted) == 0:
                student.lessons_attempted.append(tracker)
                student.attempted_results.append('Score: ' + score + '%' ' Time: ' + counter)
                student.save()
    ## if student has attempted lessons, replace the lesson appended with the new lesson
            else:
                student.lessons_attempted[0] = tracker
                student.attempted_results[0] = ('Score: ' + score + '%' ' Time: ' + counter)
                student.save()
    ## Initial load         
    else:
        current_user = request.user
        student = Student.objects.get(user_id = current_user.id)
        j = len(student.lessons_completed)
        if j < 12:
            j = len(student.lessons_completed)
            print("this if")
        else:
            j=1
            print("else")
        animal_pic = animal[j]
        animal_sound = sound[j]
        game_complete = False
        n = 1
        answer1 = 0
        correct = 0
        letter = ["a","b","c","d","e","f","g","h","i","j"]
        picture = letter[correct]
        num1 = multiplication_lesson[j][0]['num1']
        num2 = multiplication_lesson[j][0]['num2']
        num3 = multiplication_lesson[j][0 - 1]['num2']
        problem_answer = str((num1 * num3))
        tic = time.perf_counter()
    ## render the show function 
    return render (request, 'student/game.html', {'multiplication_lesson' : multiplication_lesson, 'n': n, 'answer1' : answer1, 'num1': num1, 'num2': num2, 'problem_answer': problem_answer, 'correct': correct, 'game_complete': game_complete, 'counter': counter, 'picture':picture, 'animal_pic': animal_pic, 'lesson_pass':lesson_pass, 'animal_sound':animal_sound})



# Student Welcome Page

def student_welcome(request, student_id):
    letter = ["a","b","c","d","e","f","g","h","i","j"]
## set user to current 
    current_user = request.user

    # queries the database to get the current user
    student = Student.objects.get(user_id = current_user.id)

    x = slice(len(student.lessons_completed))
    animal_array = animal[x]
## render student welcome view
    return render(request, 'student/welcome.html', {'student': student,  'animal_array': animal_array, 'letter':letter})


# Student Results View
def student_results(request):
    # get the students data based off of student id
    current_user = request.user

    # queries the database to get the current user
    student = Student.objects.get(user_id = current_user.id)

    # render the student show view
    return render (request, 'student/student_results.html', {'student': student} )


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


# Teacher View Student
@user_passes_test(lambda user: user.is_staff)
def student_show(request, classroom_id, student_id):
    # get the students data based off of student id
    student = Student.objects.get(id=student_id)

    # print('what is classroom_id from student', student.lessons_completed)

    # render the student show view
    return render (request, 'teacher/student_show.html', {'student': student})


#################################### BELOW IS NOT CURRENTLY IN USE ###############################

# class ClassroomCreate(UserPassesTestMixin, CreateView): 
#     model = Classroom
#     fields = ['name']

#     def test_func(self):
#         return self.request.user.is_staff

#     def form_valid(self, form):
#     # creating an object from the form
#         self.object = form.save(commit=False)
#         # adding a user to that object
#         self.object.user = self.request.user
#         # saving the object in the db
#         self.object.save()
#         # redirecting to the main index page
#         return HttpResponseRedirect('/teacher/classroom/')



# class StudentCreate(UserPassesTestMixin, CreateView):
#     model = Student
#     fields = "__all__"
   
#     def test_func(self):
#         return self.request.user.is_staff

#     def form_valid(self, form):
#     # creating an object from the form
#         self.object = form.save(commit=False)
#         # adding a user to that object
#         self.object.user = self.request.user
#         # saving the object in the db
#         self.object.save()
#         # redirecting to the main index page
#         return HttpResponseRedirect('/teacher/classroom/')


# # @user_passes_test(lambda user: user.is_staff)
# class StudentUpdate(UserPassesTestMixin, UpdateView,):

#     all_classrooms = ('yes', 'yes'), ('no', 'no') #Classroom.objects.all()

#     #
#     model= Student
#     fields = ['classroom','lessons_completed', 'results' ]
#     print('what is all_classrooms', all_classrooms)
 
   
  

#     def test_func(self):
#         return self.request.user.is_staff

#     # now we use a function to determine if our form data is valid
#     def form_valid(self, form):
#         # commit=False is useful when we're getting data from a form
#         # but we need to populate with some non-null data
#         # saving with commit=False gets us a model object, then we can add our extra data and save
#         self.object = form.save(commit=False)
#         self.object.save()

#         classroom = str(self.object.classroom_id)
#         # print('what is self.object', self.object.classroom_id)
#         # pk is the primary key, aka the id of the object
#         return HttpResponseRedirect('/teacher/classroom/' + classroom + '/'+ str(self.object.pk))

# #commit


