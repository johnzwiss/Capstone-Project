# Generated by Django 3.0 on 2022-04-27 19:42

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_student_lessons_attempted'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='attempted_results',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200, null=True), blank=True, default=list, size=None),
        ),
    ]
