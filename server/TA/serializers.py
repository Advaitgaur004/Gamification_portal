from rest_framework import serializers
from .models import InstructorProfile, StudentTaskStatus,Task

class InstructorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorProfile
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }
class StudentTaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentTaskStatus
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class viewTaskforStudent(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','title','description','xp_reward','deadline']


class UserSerializerWithToken_(InstructorProfileSerializer):
    access = serializers.CharField(source='access_token', read_only=True)
    refresh = serializers.CharField(source='refresh_token', read_only=True)
    class Meta:
        model = InstructorProfile
        fields = ['id', 'username', 'email', 'is_staff', 'is_active', 'access', 'refresh']


