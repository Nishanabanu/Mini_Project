# Generated by Django 5.0.7 on 2024-09-04 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_project', '0021_hostel_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hostel',
            name='COURSE',
        ),
        migrations.AddField(
            model_name='hostel',
            name='COURSE',
            field=models.ManyToManyField(to='hostel_project.course'),
        ),
    ]
