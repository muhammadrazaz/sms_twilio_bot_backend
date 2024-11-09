from django.contrib.auth.models import User,Group
from rest_framework import serializers
from auth_app.models import State
from .models import AgentProfile



class AgentSerializer(serializers.ModelSerializer):

    username = serializers.CharField()
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True,required=False)
    states = serializers.ListField(child = serializers.CharField(),write_only=True)
    state_names = serializers.SerializerMethodField() 
    
    class Meta:
        model = AgentProfile
        fields = ['id','username','password','email','channel_id','uan','states','telegram_username','state_names']
        

    def get_state_names(self, obj):

        obj = AgentProfile.objects.get(pk=obj.pk)
        return ', '.join(state.state_name for state in obj.states.all())


    def validate(self, attrs):
        
      
        super().validate(attrs)
        username = attrs.get('username','')
        instance = getattr(self, 'instance', None)
        if username:
           
            user_qs = User.objects.filter(username=username)
            if instance:
                user_qs = user_qs.exclude(pk=instance.user.pk)

            if user_qs.exists():
                raise serializers.ValidationError({"username": "Username already exists."})
        
        
        if not State.objects.filter(state_name__in = attrs['states']).exists():
            raise serializers.ValidationError({'states':'states must be valid state'})
        
        request = self.context.get('request')

        if request and request.method == 'POST':
            if 'password' not in attrs:
                raise serializers.ValidationError({"password":'this fild is required'})
            
        if 'password' in attrs and len(attrs['password']) <8:
            raise serializers.ValidationError({"password":'password must be 8 digit'})
        
        return attrs
    
    def create(self, validated_data):
        
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'] if "email" in validated_data else ''
            )
        
        user.set_password(validated_data['password'])
        group = Group.objects.filter(name="agent")
        user.groups.set(group)
        
        states = State.objects.filter(state_name__in = validated_data['states'])

        agent = AgentProfile.objects.create(
            channel_id = validated_data['channel_id'],
            user = user,
            uan = validated_data['uan'] if 'uan' in validated_data else '',
            telegram_username = validated_data['telegram_username'] if 'telegram_username' in validated_data else ''

        )

        agent.states.set(states)

        agent.username = user.username
        agent.email = user.email

        return agent
    
    def update(self, instance, validated_data):
       
        instance.user.username = validated_data.get('username')
        instance.user.email = validated_data.get('email','')
        instance.channel_id = validated_data.get('channel_id')
        instance.telegram_username = validated_data.get('telegram_username','')
        instance.uan = validated_data.get('uan','')
        instance.user.set_password(validated_data.get('password'))
        instance.user.save()
        instance.save()
        states = State.objects.filter(state_name__in = validated_data['states'])
        removed_states = instance.states.exclude(state_name__in = validated_data['states'])
        instance.states.remove(*removed_states)

        instance.states.set(states)
        

        return instance
        


   