# Generated by Django 5.1.2 on 2024-10-27 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_task_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='date',
            new_name='start_date',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='time',
            new_name='start_time',
        ),
    ]
