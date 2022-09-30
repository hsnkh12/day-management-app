from django.urls import path
from .views import (GoalView,deleteWork)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router = DefaultRouter()
router.register('goal-works', GoalView, basename='goal-works')
urlpatterns = [

    path("delete-work/<pk>/",deleteWork,name="delete-work")
    
]

urlpatterns += router.urls