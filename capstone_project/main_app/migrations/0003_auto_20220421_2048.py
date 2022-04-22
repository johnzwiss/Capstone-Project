# Generated by Django 3.0 on 2022-04-21 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_classroom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='students',
        ),
        migrations.AddField(
            model_name='student',
            name='classroom',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main_app.Classroom'),
            preserve_default=False,
        ),
    ]
