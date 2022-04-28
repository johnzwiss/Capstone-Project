from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

# Create your models here.

  

class Classroom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
  

    def __str__(self):
        return self.name

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):

    
    def response_add(self, request, obj, post_url_continue=None):
        
        return redirect('/teacher/classroom/' + str(obj.id) + '/')
        

    def response_change(self, request, obj):
        print('what is classroom.id', obj.id)
        return redirect('/teacher/classroom/' + str(obj.id) + '/')

    # def response_delete(self, request, obj):
    #     return redirect('/teacher/classroom/')

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    lessons_completed = ArrayField(base_field=models.CharField(max_length=200, null=True), default=list, blank=True)
    lessons_attempted = ArrayField(base_field=models.CharField(max_length=200, null=True), default=list, blank=True)
    results = ArrayField(base_field=models.CharField(max_length=200, null=True), default=list, blank=True)
    attempted_results = ArrayField(base_field=models.CharField(max_length=200, null=True), default=list, blank=True)

    def __str__(self):
        return str(self.user)



@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'classroom')
    
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/teacher/classroom/' + str(obj.classroom_id) + '/')

    def response_change(self, request, obj):
        print('what is obj', obj.classroom_id)
        return redirect('/teacher/classroom/' + str(obj.classroom_id) + '/' + str(obj.id) + '/')


# class TeacherAdmin(Student, admin.ModelAdmin):
#     def response_add(self, request, obj, post_url_continue=None):
#         return redirect('/teacher/classroom')

#     def response_change(self, request, obj):
#         return redirect('/teacher/classroom')