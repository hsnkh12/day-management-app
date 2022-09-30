from django.urls import path
from .views import (DayCaloriesView,DayDelete)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('day-calories',DayCaloriesView,basename="day-calories")

urlpatterns = [

    path('day-calories-delete/<pk>/',DayDelete)
    
]

urlpatterns += router.urls