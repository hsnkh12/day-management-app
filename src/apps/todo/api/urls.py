from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    DayTasksView,
    RandomTasksView,
    DayDelete
    )




router = DefaultRouter()
router.register('day-tasks', DayTasksView, basename='day-tasks')
router.register('random-tasks', RandomTasksView, basename='random-tasks')



urlpatterns = [

    path('day-tasks-delete/<pk>/',DayDelete)
    
]

urlpatterns += router.urls