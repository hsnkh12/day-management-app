from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user-notes',NoteView,basename="user-notes")



urlpatterns = [
    
]

urlpatterns += router.urls