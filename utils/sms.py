from django.contrib.auth.models import User
from celery import shared_task
from dotenv import load_dotenv
from twilio.rest import Client
import os

load_dotenv()



@shared_task(name='utils.email.send_sms_task')
def send_sms_task(instance_id, for_model, notification_type, message, title,user):
    user = User.objects.filter(id=user).first()
    # client = Client(os.environ.get('TWILIO_ACCOUNT_SID'),os.environ.get('TWILIO_AUTH_TOKEN'))

    # message = client.messages.create(
    #     body=title + message,
    #     from_ = os.environ.get('TWILIO_PHONE_NUMBER'), 
    #     to = '+923015987322'
    #     to = user.agentprofile.uan
    # )
    print("Sending SMS...")