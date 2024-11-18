from rest_framework import serializers
from auth_app.models import State,Notification,User
from .models import Lead,Shipping


class LeadSerializer(serializers.ModelSerializer):
    state_names = serializers.ListField(child=serializers.CharField())
    states = serializers.CharField(read_only=True)
    class Meta:
        model = Lead
        fields = '__all__'


    def validate(self, attrs):
 
        super().validate(attrs)

        state_names = attrs.pop('state_names')
       

        if State.objects.filter(state_name__in=state_names).count() != len(set(state_names)):
            raise serializers.ValidationError({'state_names': 'All provided states must be valid.'})
        
        # attrs['states'] = State.objects.filter(state_name__in=state_names)
        attrs['states'] = state_names
        return attrs
    
    def create(self, validated_data):
    
        lead_states = validated_data.pop('states')
      
        states = State.objects.filter(state_name__in = lead_states)
        lead = Lead.objects.create(**validated_data)
       
        lead.states.set(states)
        print('===================  ')
        lead.save()
        
        lead.state_names = lead_states
        return lead
    
    def update(self, instance, validated_data):
       
        lead_states = validated_data.pop('states', None)

       
        instance = super().update(instance=instance,validated_data=validated_data)

        if lead_states is not None:
            
            current_states = instance.states.all()

           
            new_states = State.objects.filter(state_name__in=lead_states)

            
            states_to_add = new_states.exclude(id__in=[state.id for state in current_states])

           
            states_to_remove = current_states.exclude(state_name__in=lead_states)

            

           
            if states_to_add.exists():
                instance.states.add(*states_to_add)

           
            if states_to_remove.exists():
                instance.states.remove(*states_to_remove)

        
        instance.state_names = lead_states
        instance.save()

        return instance

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'


class BotLeadSerializer(serializers.ModelSerializer):
    user_states = serializers.CharField()
    
    class Meta:
        model = Lead
        fields = ['id','user_id','username','whatsapp','sms','email','discord','instagram','snapchat','user_states','status']
        # fields = '__all__'
        

    def validate(self, attrs):
        super().validate(attrs)

        user_states = attrs.get('user_states')
        user_states = user_states.split(',')

        if not isinstance(user_states, list):
            user_states = [user_states.stripe()]
        else:
            user_states = [state.strip() for state in user_states]

       

        if State.objects.filter(state_name__in=user_states).count() != len(set(user_states)):
            raise serializers.ValidationError({'user_states': 'All provided states must be valid.'})
        
        attrs['states'] = user_states
        attrs.pop('user_states')
        return attrs
    

    def create(self, validated_data):
        states = validated_data.pop('states')
        states = State.objects.filter(state_name__in = states)
        
        lead = Lead.objects.create(**validated_data)
        lead.states.set(states)

        states = State.objects.filter(lead = lead.id).values_list('state_name',flat=True)

        lead.user_states = ','.join(states)
        

        return lead


class BotShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'


class BotStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'
