from django_celery_beat.models import PeriodicTask, ClockedSchedule
from django.db.models.signals import post_save, pre_save
from datetime import datetime,timedelta
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Q
from task.models import Task
import json
import pytz

@receiver(post_save, sender=Task)
def task_save_handler(sender, instance, created, **kwargs):
    local_dt = datetime.strptime(f"{instance.start_date} {instance.start_time}", "%Y-%m-%d %H:%M:%S")
    local_tz = pytz.timezone(instance.user_timezone)  # Replace with your timezone if different
    local_dt = local_tz.localize(local_dt)
    utc_dt = local_dt.astimezone(pytz.UTC)

    utc_dt = utc_dt - timedelta(minutes=1)
   
    if created:
        clocked_schedule, created = ClockedSchedule.objects.get_or_create(clocked_time=utc_dt)

        
        PeriodicTask.objects.create(
            name=f'Send In App Notification Task {instance.id}', 
            task='utils.notification.send_notification_task',  
            one_off=True,  
            clocked=clocked_schedule,  
            args=json.dumps([instance.id,'task','in_app_notification',f"Your task '{instance.title}' is due at {instance.start_time} {instance.start_date}.{instance.description}.",'Task Reminder',instance.user.id]),
            expires=utc_dt+timedelta(minutes=10), 
            kwargs=json.dumps({})  
        )

        if instance.user.groups.filter(name="agent").exists():
            if instance.user.agentprofile.uan:
                PeriodicTask.objects.create(
                name=f'Send sms Notification Task {instance.id}', 
                task='utils.sm.send_sms_task',  
                one_off=True,  
                clocked=clocked_schedule,  
                args=json.dumps([instance.id,'task','sms_notification',f"Your task '{instance.title}' is due at {instance.start_time} {instance.start_date}.{instance.description}.",'Task Reminder',instance.user.id]),
                expires=utc_dt+timedelta(minutes=10),    
                kwargs=json.dumps({})  
                )

        elif instance.user.email:

            PeriodicTask.objects.create(
            name=f'Send Email Notification Task {instance.id}', 
            task='utils.email.send_email_task',  
            one_off=True,  
            clocked=clocked_schedule,  
            args=json.dumps([instance.id,'task','email_notification',f"Your task '{instance.title}' is due at {instance.start_time} {instance.start_date}.{instance.description}.",'Task Reminder',instance.user.id]),
            expires=utc_dt+timedelta(minutes=10),    
            kwargs=json.dumps({})  
            )

     
        print("New instance created:", instance)

@receiver(pre_save, sender=Task)
def capture_old_values(sender, instance, **kwargs):
    
    if instance.pk:  

        old_instance = sender.objects.get(pk=instance.pk)
        
     
        periodic_tasks = PeriodicTask.objects.filter(
            Q(args__icontains=str(old_instance.id)) &  
            Q(args__icontains='task') &  
            Q(args__icontains=f"Your task '{old_instance.title}' is due at {old_instance.start_time} {old_instance.start_date}.{old_instance.description}.") &  
            Q(args__icontains=old_instance.title) &  
            Q(args__icontains=str(old_instance.user.id)) 
        )
      
        if periodic_tasks.exists():
            local_dt = datetime.strptime(f"{instance.start_date} {instance.start_time}", "%Y-%m-%d %H:%M:%S")
            local_tz = pytz.timezone(instance.user_timezone) 
            local_dt = local_tz.localize(local_dt)
            utc_dt = local_dt.astimezone(pytz.UTC)

        
            clocked_schedule, _ = ClockedSchedule.objects.get_or_create(clocked_time=utc_dt - timedelta(minutes=1))
            for periodic_task in periodic_tasks:
              
                existing_args = json.loads(periodic_task.args)

               
                new_args = [
                    existing_args[0], 
                    existing_args[1],  
                    existing_args[2],  
                    f"Your task '{instance.title}' is due at {instance.start_time} {instance.start_date}.{instance.description}.", 
                    existing_args[4], 
                    existing_args[5]   
                ]
                periodic_task.clocked = clocked_schedule
                periodic_task.args = json.dumps(new_args)
                periodic_task.save()  
                periodic_task.clocked.save()
       




































        # target_args = json.dumps([
        #     old_instance.id, 
        #     'task', 
        #     'in_app_notification', 
        #     f"your task is due at {old_instance.start_time} {old_instance.start_date}", 
        #     old_instance.title,
        #     old_instance.user.id
        # ])
    
        # periodic_tasks = PeriodicTask.objects.filter(args=target_args)
        
        # if periodic_tasks.exists():
        #     for periodic_task in periodic_tasks:
               
        #         local_dt = datetime.strptime(f"{instance.start_date} {instance.start_time}", "%Y-%m-%d %H:%M:%S")
        #         local_tz = pytz.timezone(instance.user_timezone) 
        #         local_dt = local_tz.localize(local_dt)
        #         utc_dt = local_dt.astimezone(pytz.UTC)

           
        #         clocked_schedule, _ = ClockedSchedule.objects.get_or_create(clocked_time=utc_dt - timedelta(minutes=1))
                
        #         periodic_task.clocked = clocked_schedule
        #         periodic_task.args = json.dumps([
        #             instance.id, 
        #             'task', 
        #             'in_app_notification', 
        #             f"your task is due at {instance.start_time} {instance.start_date}", 
        #             instance.title,
        #             instance.user.id
        #         ])
        #         periodic_task.save()  # Save the changes
        #         periodic_task.clocked.save()

        # target_args = json.dumps([
        #     old_instance.id, 
        #     'task', 
        #     'in_app_notification', 
        #     f"your task is due at {old_instance.start_time} {old_instance.start_date}", 
        #     old_instance.title,
        #     old_instance.user.id
        # ])
    
        # periodic_tasks = PeriodicTask.objects.filter(args=target_args)
        
        # if periodic_tasks.exists():
        #     for periodic_task in periodic_tasks:
               
        #         local_dt = datetime.strptime(f"{instance.start_date} {instance.start_time}", "%Y-%m-%d %H:%M:%S")
        #         local_tz = pytz.timezone(instance.user_timezone) 
        #         local_dt = local_tz.localize(local_dt)
        #         utc_dt = local_dt.astimezone(pytz.UTC)

           
        #         clocked_schedule, _ = ClockedSchedule.objects.get_or_create(clocked_time=utc_dt - timedelta(minutes=1))
                
        #         periodic_task.clocked = clocked_schedule
        #         periodic_task.args = json.dumps([
        #             instance.id, 
        #             'task', 
        #             'in_app_notification', 
        #             f"your task is due at {instance.start_time} {instance.start_date}", 
        #             instance.title,
        #             instance.user.id
        #         ])
        #         periodic_task.save()  # Save the changes
        #         periodic_task.clocked.save()