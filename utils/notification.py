from celery import shared_task

@shared_task(name='utils.notification.send_notification_task')
def send_notification_task(instance_id, for_model, notification_type, message, title,user):
    from django.contrib.auth.models import User
    from auth_app.models import Notification
    user = User.objects.get(id=user)
    Notification.objects.create(user=user,model=for_model,model_id = instance_id,title=title,description=message)
    print("Sending notification...")

