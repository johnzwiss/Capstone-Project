from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.postgres.fields import ArrayField

# Create your models here.

  

class Classroom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
  

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    lessons_completed = ArrayField(base_field=models.CharField(max_length=200, null=True), default=list, blank=True)
    results = ArrayField(base_field=models.CharField(max_length=200, null=True), default=list, blank=True)

    def __str__(self):
        return str(self.user)


