from rest_framework.response import Response
from rest_framework import status
from ..todo.api.serializers import DayTasksSerializer,TaskSerializer
from rest_framework.viewsets import ViewSet
from ..todo.models import Task
from django.shortcuts import (
    get_object_or_404
    )

from ..abstraction.utils import (
    ValidationCheck,
    ValidateDate,)
from rest_framework import status,response



class TasksView(ViewSet):

    def update(self,request,pk=None):

        queryset = get_object_or_404(Task, pk=pk)

        if queryset.day_tasks.user != request.user:
            return response(status = status.HTTP_401_UNAUTHORIZED)

        serializer = TaskSerializer( queryset ,data = request.data )
        return ValidationCheck(serializer)


    def destroy(self,request,pk=None):
        
        queryset = get_object_or_404(Task, pk=pk)

        if queryset.day_tasks.user != request.user:
            return response(status = status.HTTP_401_UNAUTHORIZED)
            
        queryset.delete()

        return Response(status=status.HTTP_200_OK)