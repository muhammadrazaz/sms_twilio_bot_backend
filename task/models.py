from django.db import models
from auth_app.models import TimestampedModel
from django.contrib.auth.models import User



class Task(TimestampedModel):
    category_choices = (
        ('email','Email'),
        ('call','Call'),
    )
    status_choices = (
        ('pending','Pending'),
        ('started','Started'),
        ('completed','Completed')
    )

    priority_choices = (
        ('high','High'),
        ('medium','Medium'),
        ('low','Low')
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50,choices=category_choices)
    start_date = models.DateField()
    start_time = models.TimeField()
    status = models.CharField(max_length=50,choices=status_choices,default='pending')
    priority = models.CharField(max_length=30,choices=priority_choices,default='medium')
    description = models.CharField(max_length=500,blank=True,null=True)
    user_timezone = models.CharField(max_length=50,default='Asia/Karachi')

    @classmethod
    def get_status_choices(cls):
        return [display for _, display in cls.status_choices]
    
    @classmethod
    def get_category_choices(cls):
        return [display for _, display in cls.category_choices]
    
    @classmethod
    def get_priority_choices(cls):
        return [display for _, display in cls.priority_choices]
