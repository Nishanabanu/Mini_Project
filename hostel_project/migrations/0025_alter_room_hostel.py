# Generated by Django 5.0.7 on 2024-09-05 16:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_project', '0024_alter_room_hostel_alter_room_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='HOSTEL',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hostel_project.hostel'),
            preserve_default=False,
        ),
    ]
