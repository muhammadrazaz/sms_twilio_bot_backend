from django.contrib.auth.models import User
from django.core.mail import send_mail
from celery import shared_task
from dotenv import load_dotenv
import os


load_dotenv()
@shared_task(name='utils.email.send_email_task')
def send_email_task(instance_id, for_model, notification_type, message, title,user):
    user = User.objects.filter(id=user).first()
    send_mail(
            title,
            message,
            os.environ.get('DEFAULT_FROM_EMAIL'),
            [user.email],
            fail_silently=False,
        )

    print("Sending email...")

