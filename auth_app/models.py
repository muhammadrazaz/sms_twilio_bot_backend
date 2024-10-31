from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the first time the object is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically update every time the object is saved

    class Meta:
        abstract = True

class State(TimestampedModel):
    state_name  = models.CharField(max_length=50,unique=True)

class Notification(TimestampedModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    is_read_choices = ((True,'true'),(False,'false'))
    model = models.CharField(max_length=50)
    model_id = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    is_read = models.CharField(max_length=10,choices=is_read_choices,default=False)

class Bot(TimestampedModel):
  
    bot_id = models.CharField(max_length=50,blank=False,unique=True)
    telegram_username = models.CharField(max_length=50,blank=False)
    bot_father_token = models.CharField(max_length=255,blank=False)
    bot_url = models.CharField(max_length=255,blank=False)
    server_username = models.CharField(max_length=255,blank=True)
    server_password = models.CharField(max_length=255,blank=True)
    instance_dns = models.CharField(max_length=255,blank=True)
    instance_username = models.CharField(max_length=255,blank=True)
    instance_password = models.CharField(max_length=255,blank=True)
    database_backup = models.FileField(upload_to='backup',blank=True,null=True)
    


    
