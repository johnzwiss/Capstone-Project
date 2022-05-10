from tokenize import Number
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

# Create your models here.

  
# Classroom Model Creation
class Classroom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
  

    def __str__(self):
        return self.name

# Extends the model on the Admin Page
@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):

    # fields = ['name']
    # modifies the forms used for classroom
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Sets the initial value of the user field to the logged in user's id
        form.base_fields["user"].initial = request.user.id
        return form

    # changes default redirect to the classroom page
    def response_add(self, request, obj, post_url_continue=None):
        
        return redirect('/teacher/classroom/' + str(obj.id) + '/')
        
    # changes default redirect to the classroom page
    def response_change(self, request, obj):
        print('what is classroom.id', obj.id)
        return redirect('/teacher/classroom/' + str(obj.id) + '/')

# initilization of the Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    lessons_completed = ArrayField(base_field=models.CharField(max_length=200, null=True), default=list, blank=True)
    lessons_attempted = ArrayField(base_field=models.CharField(max_length=200, null=True), default=list, blank=True)
    results = ArrayField(base_field=models.CharField(max_length=200, null=True), default=list, blank=True)
    attempted_results = ArrayField(base_field=models.CharField(max_length=200, null=True), default=list, blank=True)
    problem_number= models.IntegerField(blank=True, null=True)
    correct = models.IntegerField(blank=True, null=True)
    ##correct
    ##global variable resets in heroku, need to access variables through saved student model. 
    # if Model is referenced return the string of the user
    def __str__(self):
        return str(self.user)


# Extends the model on the Admin Page
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # adds a column in the students page of the Admin page
    list_display = ('user', 'classroom')
    # Limits which fields are visible and editable
    fields = ['user', 'classroom', 'lessons_completed' , 'results']

    # modifies the forms used for Student
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # changes the label for user to indicate a new user account will need to be created. 
        form.base_fields["user"].label = 'User:(click + to create student account)'
        return form
    
     # changes default redirect to the classroom page
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/teacher/classroom/' + str(obj.classroom_id) + '/')

     # changes default redirect to the student's show page
    def response_change(self, request, obj):
        print('what is obj', obj.classroom_id)
        return redirect('/teacher/classroom/' + str(obj.classroom_id) + '/' + str(obj.id) + '/')


