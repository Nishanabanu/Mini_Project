# Generated by Django 5.0.7 on 2024-09-04 16:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_project', '0020_remove_student_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostel',
            name='COURSE',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hostel_project.course'),
            preserve_default=False,
        ),
    ]