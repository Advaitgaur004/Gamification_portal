from rest_framework import viewsets
from .models import InstructorProfile, StudentTaskStatus,Task
from .serializers import InstructorProfileSerializer, StudentTaskStatusSerializer, TaskSerializer

class InstructorProfileViewSet(viewsets.ModelViewSet):
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorProfileSerializer

class StudentTaskStatusViewSet(viewsets.ModelViewSet):
    queryset = StudentTaskStatus.objects.all()
    serializer_class = StudentTaskStatusSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer