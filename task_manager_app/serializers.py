from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, TaskStatus


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='status.status')
    created_at = serializers.DateTimeField(format="%d %B %Y, %I:%M %p")

    class Meta:
        model = Task
        fields = "__all__"


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
