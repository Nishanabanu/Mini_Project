# Generated by Django 5.0.7 on 2024-08-03 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_project', '0007_remove_parent_image_remove_student_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warden',
            name='HOSTEL',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hostel_project.hostel'),
        ),
    ]