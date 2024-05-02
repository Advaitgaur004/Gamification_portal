from rest_framework import viewsets
from .models import Badge, StudentProfile,Extra
from .serializers import BadgeSerializer, StudentProfileSerializer, UserSerializerWithToken
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework import generics, mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import serializers
from TA.models import Task
from TA.serializers import viewTaskforStudent
from datetime import datetime, timedelta
from django.db.models import Count

class BadgeViewSet(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class StudentProfileViewSet(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RegisterUserView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = StudentProfileSerializer

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            if StudentProfile.objects.filter(email=data['email']).exists():
                raise ValueError('User with this email already exists')
            if StudentProfile.objects.filter(Rollno=data['Rollno']).exists():
                raise ValueError('User with this Rollno already exists')

            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )

            student_profile = StudentProfile.objects.create(
                username=data['username'],
                Rollno=data['Rollno'],
                email=data['email'],
                password=make_password(data['password']),
                total_xp=0
            )
            Extra.objects.create(user=user, student=student_profile)
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            student_profile.refreshtoken = refresh_token
            student_profile.save()
            serializer = self.get_serializer(student_profile)

            return Response({
                "refresh": refresh_token,
                "access": access_token,
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            message = {'detail': str(e)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
class UserProfileViewSet(generics.GenericAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self,request, *args, **kwargs):
        user = StudentProfile.objects.get(email=request.user.email)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        serializer = UserSerializerWithToken(user)
        data.update(serializer.data)

        return data
    def get_token(self, user):
        return super().get_token(user)
    
class MyTokenObtainPairView(APIView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # print(request.user)
        # student = Extra.objects.all().filter(user=request.user)
        # print(student)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

class TokenRefreshSerializers(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['refreshtoken']

class TokenRefreshView(GenericAPIView, mixins.CreateModelMixin):
    serializer_class = TokenRefreshSerializers
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
        
#TODO: for testing purpose
class ViewTaskViewSet(GenericAPIView, mixins.ListModelMixin):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = StudentProfile.objects.get(email=request.user.email)
        task_ids = user_profile.tasks.values_list('id', flat=True)
        tasks = Task.objects.filter(id__in=task_ids)
        serializer = viewTaskforStudent(tasks, many=True)  # Assuming you have a TaskSerializer for the Task model

        for task in serializer.data:
            deadline = datetime.strptime(task['deadline'], "%Y-%m-%dT%H:%M:%S%z")
            first_day = deadline.replace(day=1)
            first_monday = (first_day.weekday() - 0) % 7
            second_monday = first_day + timedelta(days=(7 - first_monday) + 7)
            task['deadline'] = second_monday.strftime("%A, %B %d, %Y %I:%M %p")

        return Response(serializer.data)

class LeaderBoardXP(APIView):
    def get(self, request):
        students = StudentProfile.objects.all().order_by('-total_xp')
        serializer = StudentProfileSerializer(students, many=True)
        return Response(serializer.data)

class LeaderBoardBadge(APIView):
    def get(self, request):
        students = StudentProfile.objects.annotate(num_badges=Count('badge')).order_by('-num_badges')
        serializer = StudentProfileSerializer(students, many=True)
        return Response(serializer.data)