from django.db.models.signals import post_save,m2m_changed
from django.dispatch import receiver
from .models import Lead,Shipping
from auth_app.models import User,Notification

# @receiver(post_save, sender=Lead)
@receiver(m2m_changed, sender=Lead.states.through)
def states_set_handler(sender, instance, action, **kwargs):
  
    if action == 'post_add': 
       
        lead_states  = instance.states.values_list('state_name', flat=True)
        
        admins = User.objects.filter(groups__name='admin')
        for user in admins:
            Notification.objects.create(user=user,model="leads",model_id = instance.id,title="New InTown lead",description=f"New lead is created for "+','.join(lead_states))

        agents = User.objects.filter(agentprofile__states__state_name__in=lead_states).distinct()
        for user in agents:
            Notification.objects.create(user=user,model="leads",model_id = instance.id,title="New InTown lead",description=f"New lead is created for "+','.join(lead_states))

@receiver(post_save, sender=Shipping)
def states_set_handler(sender, instance, created, **kwargs):
    if created:
        users = User.objects.all()
        for user in users:
            Notification.objects.create(user=user,model="shippings",model_id = instance.id,title="New shipping lead",description=f"New shipping lead is created.")