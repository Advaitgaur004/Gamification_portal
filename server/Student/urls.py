from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BadgeViewSet, StudentProfileViewSet, RegisterUserView, UserProfileViewSet, MyTokenObtainPairView,ViewTaskViewSet
from .views import TokenRefreshView,LeaderBoardXP,LeaderBoardBadge


urlpatterns = [
    path('badges',BadgeViewSet.as_view()),
    path('student_profiles',StudentProfileViewSet.as_view()),
    path('register/', RegisterUserView.as_view()),
    path('profile/',UserProfileViewSet.as_view()), #have to look
    path('token/', MyTokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('tasks',ViewTaskViewSet.as_view()),
    path('leaderboard/xp',LeaderBoardXP.as_view()),
    path('leaderboard/badge',LeaderBoardBadge.as_view())
]

