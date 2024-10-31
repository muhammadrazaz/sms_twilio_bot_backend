from rest_framework import serializers
from auth_app.models import State
from .models import Lead,Shipping

class LeadSerializer(serializers.ModelSerializer):
    state_names = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Lead
        fields = '__all__'


    def validate(self, attrs):
        super().validate(attrs)

        state_names = attrs.get('state_names')
       

        if State.objects.filter(state_name__in=state_names).count() != len(set(state_names)):
            raise serializers.ValidationError({'state_names': 'All provided states must be valid.'})
        
        attrs['states'] = State.objects.filter(state_name__in=state_names)
        
        return attrs
    
    def create(self, validated_data):
        states = validated_data.pop('states')
        states = State.objects.filter(state_name__in = states)
        lead = Lead.objects.create(**validated_data)
        lead.states.set(states)
        

        return lead

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'


class BotLeadSerializer(serializers.ModelSerializer):
    user_states = serializers.CharField()
    
    class Meta:
        model = Lead
        fields = ['id','user_id','whatsapp','sms','email','discord','instagram','snapchat','user_states']
        # fields = '__all__'
        

    def validate(self, attrs):
        super().validate(attrs)

        user_states = attrs.get('user_states')
        user_states = user_states.split(',')

        if not isinstance(user_states, list):
            user_states = [user_states]

       

        if State.objects.filter(state_name__in=user_states).count() != len(set(user_states)):
            raise serializers.ValidationError({'user_states': 'All provided states must be valid.'})
        
        attrs['states'] = user_states
        
        return attrs
    

    def create(self, validated_data):
        states = validated_data.pop('states')
        states = State.objects.filter(state_name__in = states)
        lead = Lead.objects.create(**validated_data)
        lead.states.set(states)
        

        return lead


class BotShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'
