# Generated by Django 5.1.2 on 2024-10-27 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('email', 'Email'), ('call', 'Call')], max_length=50)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('started', 'Started'), ('completed', 'Completed')], default='pending', max_length=50)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]