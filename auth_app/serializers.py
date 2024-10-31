from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import State,Bot

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    access_token = serializers.CharField(read_only = True)
    refresh_token = serializers.CharField(read_only = True)
    role = serializers.CharField(read_only = True)
    username = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','access_token','refresh_token','role']
        read_only_fields = ['first_name','last_name','email']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=False)
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password_confirm','role')

    def get_role(self, obj):
       
        return obj.groups.first().name if obj.groups.exists() else ''

    def validate(self, data):
       
        if data.get('password') and data['password'] != data.get('password_confirm'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def update(self, instance, validated_data):
       
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)

   
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
    
class BotDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = '__all__'





