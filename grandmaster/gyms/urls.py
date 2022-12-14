from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GymViewSet, TrainersList

router = DefaultRouter()
router.register('', GymViewSet, basename='gyms')

urlpatterns = [
    path('trainers/', TrainersList.as_view()),
    path('', include(router.urls)),
]
