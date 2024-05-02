from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from Student.views import LeaderBoardBadge,LeaderBoardXP,BadgeViewSet
urlpatterns = [
    path('instructor_profiles',InstructorProfileViewSet.as_view()),
    path('student_task_status',StudentTaskStatusViewSet.as_view()),
    path('tasks',TaskViewSet.as_view()),
    path('modify_task/<int:pk>',ModifyTaskViewSet.as_view()),
    path('register/', RegisterFacultyView.as_view()),
    path('profile/',FacultyProfileViewSet.as_view()), 
    path('token/', MyTokenObtainPairView_faculty.as_view()),
    path('refresh/', FacultyTokenRefreshView.as_view()),
    path('leaderboard/xp',LeaderBoardXP.as_view()),
    path('leaderboard/badge',LeaderBoardBadge.as_view()),
    path('badges',BadgeViewSet.as_view()),
]
