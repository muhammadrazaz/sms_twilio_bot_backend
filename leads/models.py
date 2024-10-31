from django.db import models
from auth_app.models import State,TimestampedModel
# Create your models here.

class Lead(TimestampedModel):
    status_choices = (
    ('in_progress', 'In Progress'), 
    ('not_verified', 'Not Verified'), 
    ('verified', 'Verified')
)
    

    user_id = models.CharField(max_length=50,unique=True)
    username = models.CharField(max_length=50,blank=True,null=True)
    whatsapp = models.CharField(max_length=20,blank=True,null=True)
    sms = models.CharField(max_length=20,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    discord = models.CharField(max_length=30,blank=True,null=True)
    instagram = models.CharField(max_length=30,blank=True,null=True)
    snapchat = models.CharField(max_length=30,blank=True,null=True)
    status = models.CharField(max_length=20,choices=status_choices,default='in_progress')
    states = models.ManyToManyField(State)
    notes = models.CharField(max_length=500,blank=True,null=True)

    def get_state_names(self):
        
        return ', '.join(State.state_name for state in self.states.all())
    
    @classmethod
    def get_status_choices(cls):
        return [display for _, display in cls.status_choices]

class Shipping(TimestampedModel):
    status_choices = (
    ('in_progress', 'In Progress'), 
    ('not_verified', 'Not Verified'), 
    ('verified', 'Verified')
)
    

    user_id = models.CharField(max_length=50,unique=True)
    whatsapp = models.CharField(max_length=20,blank=True,null=True)
    sms = models.CharField(max_length=20,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    discord = models.CharField(max_length=30,blank=True,null=True)
    instagram = models.CharField(max_length=30,blank=True,null=True)
    snapchat = models.CharField(max_length=30,blank=True,null=True)
    status = models.CharField(max_length=20,choices=status_choices,default='in_progress')
    notes = models.CharField(max_length=500,blank=True,null=True)

    @classmethod
    def get_status_choices(cls):
        return [display for _, display in cls.status_choices]
    