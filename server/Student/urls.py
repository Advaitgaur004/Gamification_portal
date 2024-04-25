from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BadgeViewSet, StudentProfileViewSet

router = DefaultRouter()
router.register(r'badges', BadgeViewSet)
router.register(r'student-profiles', StudentProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
