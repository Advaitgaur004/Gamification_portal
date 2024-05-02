from rest_framework import serializers
from .models import StudentProfile, Badge
from django.contrib.auth.password_validation import validate_password

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['id', 'username', 'email', 'Rollno', 'password', 'badge', 'tasks', 'total_xp']
        read_only_fields = ['id', 'badge', 'tasks', 'total_xp', 'is_staff', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'Rollno': {'required': True},
        }

class UserSerializerWithToken(StudentProfileSerializer):
    access = serializers.CharField(source='access_token', read_only=True)
    refresh = serializers.CharField(source='refresh_token', read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['id', 'username', 'email', 'badge', 'tasks', 'total_xp', 'is_staff', 'is_active', 'access', 'refresh']
