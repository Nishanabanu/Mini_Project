# Generated by Django 5.0.7 on 2024-07-31 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_project', '0002_student_hostel'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostel',
            name='image',
            field=models.FileField(default=1, upload_to='hostel_images/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hostel',
            name='status',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]