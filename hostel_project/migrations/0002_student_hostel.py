# Generated by Django 5.0.7 on 2024-07-30 17:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='HOSTEL',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hostel_project.hostel'),
            preserve_default=False,
        ),
    ]
