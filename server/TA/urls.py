from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from Student.views import LeaderBoardBadge,LeaderBoardXP,BadgeViewSet
urlpatterns = [
    path('instructor_profiles',InstructorProfileViewSet.as_view()),
    path('student_task_status',StudentTaskStatusViewSet.as_view()),
    path('tasks',TaskViewSet.as_view()),
    path('modify_task/<int:pk>',ModifyTaskViewSet.as_view()),
    path('register/', RegisterUserView.as_view()),
    path('profile/',UserProfileViewSet.as_view()), 
    path('token/', MyTokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('leaderboard/xp',LeaderBoardXP.as_view()),
    path('leaderboard/badge',LeaderBoardBadge.as_view()),
    path('badges',BadgeViewSet.as_view()),
]
