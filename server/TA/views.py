from rest_framework import viewsets
from .models import InstructorProfile, StudentTaskStatus,Task, Extra_TA
from .serializers import InstructorProfileSerializer, StudentTaskStatusSerializer, TaskSerializer,UserSerializerWithToken
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

class InstructorProfileViewSet(viewsets.ModelViewSet):
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorProfileSerializer

class StudentTaskStatusViewSet(viewsets.ModelViewSet):
    queryset = StudentTaskStatus.objects.all()
    serializer_class = StudentTaskStatusSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class RegisterUserView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = InstructorProfileSerializer

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            if InstructorProfile.objects.filter(email=data['email']).exists():
                raise ValueError('User with this email already exists')

            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
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

class UserProfileViewSet(generics.GenericAPIView):
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self,request, *args, **kwargs):
        user = InstructorProfile.objects.get(email=request.user.email)
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
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

class TokenRefreshSerializers(serializers.ModelSerializer):
    class Meta:
        model = InstructorProfile
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


   