from rest_framework import viewsets
from Student.models import StudentProfile
from .models import InstructorProfile, StudentTaskStatus,Task, Extra_TA
from .serializers import InstructorProfileSerializer, StudentTaskStatusSerializer, TaskSerializer,UserSerializerWithToken_
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status,mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist


class InstructorProfileViewSet(GenericAPIView, mixins.ListModelMixin):
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorProfileSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class StudentTaskStatusViewSet(GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = StudentTaskStatus.objects.all()
    serializer_class = StudentTaskStatusSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'You are not authorized to view this'}, status=status.HTTP_400_BAD_REQUEST)
        task_id = request.data.get('task')
        student_id = request.data.get('student')
        student = StudentProfile.objects.get(id=student_id)

        try:
            if request.data.get('completed') == 'true':
                student.tasks.remove(task_id)
                student.total_xp += Task.objects.get(id=task_id).xp_reward
                student.save()

            return self.create(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({'Task Mismatches with students'},status=status.HTTP_404_NOT_FOUND)
class TaskViewSet(GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
class ModifyTaskViewSet(GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            task = Task.objects.get(pk=pk)
            if task:
                if 'title' in request.data:
                    task.title = request.data['title'] or task.title
                if 'description' in request.data:
                    task.description = request.data['description'] or task.description
                if 'xp_reward' in request.data:
                    task.xp_reward = request.data['xp_reward'] or task.xp_reward
                if 'deadline' in request.data:
                    task.deadline = request.data['deadline'] or task.deadline
                task.save()
                serializer = self.get_serializer(task)
                return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response({'Task Deleted'}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    
class RegisterFacultyView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = InstructorProfileSerializer

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            if InstructorProfile.objects.filter(email=data['email']).exists():
                raise ValueError('User with this email already exists')

            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                is_staff=True
            )

            Instructor_profile = InstructorProfile.objects.create(
                username=data['username'],
                email=data['email'],
                password=make_password(data['password']),
            )
            Extra_TA.objects.create(user=user, faculty=Instructor_profile)
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            Instructor_profile.refreshtoken = refresh_token
            Instructor_profile.save()
            serializer = self.get_serializer(Instructor_profile)

            return Response({
                "refresh": refresh_token,
                "access": access_token,
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            message = {'detail': str(e)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
class FacultyProfileViewSet(generics.GenericAPIView):
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self,request, *args, **kwargs):
        try :
            user = InstructorProfile.objects.get(email=request.user.email)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'You are Not a faculty'}, status=status.HTTP_404_NOT_FOUND)

class MyTokenObtainPairSerializer_faculty(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        serializer = UserSerializerWithToken_(user)
        data.update(serializer.data)

        return data
    def get_token(self, user):
        return super().get_token(user)
    
class MyTokenObtainPairView_faculty(APIView):
    serializer_class = MyTokenObtainPairSerializer_faculty

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

class TokenRefreshSerializers_faculty(serializers.ModelSerializer):
    class Meta:
        model = InstructorProfile
        fields = ['refreshtoken']

class FacultyTokenRefreshView(GenericAPIView, mixins.CreateModelMixin):
    serializer_class = TokenRefreshSerializers_faculty
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refreshtoken')
        if refresh_token:
            try:
                refresh_token_obj = RefreshToken(refresh_token)
                new_access_token = str(refresh_token_obj.access_token)
                
                return Response(new_access_token)
            
            except Exception as e:
                return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)


