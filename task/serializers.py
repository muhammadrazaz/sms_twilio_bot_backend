from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),required=False)
    class Meta:
        model = Task
        fields = '__all__'

        
    def create(self, validated_data):
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user
        return super().update(instance, validated_data)