from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lessons_completed = ArrayField(base_field=models.CharField(max_length=200, null=True), default=list, blank=True)




