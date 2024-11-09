from django.db import models
from django.contrib.auth.models import User
from auth_app.models import State,TimestampedModel
from django.core.validators import RegexValidator
# Create your models here.

uan_regex = RegexValidator(
    regex=r'^\+?1?\d{10}$',
    message="Phone number must be entered in the format: '+1XXXXXXXXXX' or 'XXXXXXXXXX'."
)

class AgentProfile(TimestampedModel):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    channel_id  = models.CharField(max_length=100,unique=False)
    telegram_username = models.CharField(max_length=50,blank=True,null=True)
    uan = models.CharField(max_length=12,blank=True,null=True,validators=[uan_regex])
    states = models.ManyToManyField(State)

    class Meta:
        db_table = 'agent_profile'





