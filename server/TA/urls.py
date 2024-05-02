from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstructorProfileViewSet,StudentTaskStatusViewSet,TaskViewSet
from .views import MyTokenObtainPairView,TokenRefreshView
router = DefaultRouter()

router.register(r'instructor-profiles', InstructorProfileViewSet)
router.register(r'student-task-statuses', StudentTaskStatusViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('register/', registerUser),
    # path('profile/',getUserProfile,name='user-profile'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
