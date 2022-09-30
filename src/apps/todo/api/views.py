from django.shortcuts import get_object_or_404

from ...abstraction.utils import (
    ValidationCheck,
    ValidateDate,
    CheckQueryParm,GetDay,GetQueryInCreate)

from ..utils import TasksView
from rest_framework import status,serializers
from rest_framework.response import Response
from .serializers import DayTasksSerializer,TaskSerializer
from ..models import DayTasks,Task
from rest_framework.views import APIView

from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view


class DayTasksView(TasksView):      # Day-tasks enpoint to manage days and tasks       

    permission_classes = [
        IsAuthenticated,
    ]
    

    def list(self,request):     # We use list func because we either list days or list tasks based on the query param

        query_par = self.get_query_parameter() 
        date = CheckQueryParm(query_par,"date",other=False)
        

        if date:       # It means that we are triggering a specific day wether in calander or other

            ValidateDate(date)      # Checking it the date is in the right format
            data = GetDay(self.get_queryset, query_par, date, app="todo")      

            data_RESPONSE = {

                "Day" : DayTasksSerializer(
                    data['day'],
                    ).data,

                "Tasks" : TaskSerializer(
                    data['tasks'],
                    many=True,
                    fields=("id","text","time","completed","important")
                    ).data
            }       

        else:       # No specidic day (list of days)

            queryset = DayTasks.objects.get_days_related(request.user).order_by("date")      # Getting list of days related to user

            data_RESPONSE = {
                "Days" : DayTasksSerializer(
                    queryset,
                    fields=("id","date","rate","expired"),
                    many=True
                    ).data
            }

        return Response(data_RESPONSE)


    def create(self,request):       # Creat new task in day tasks

        query_par = self.get_query_parameter()
        queryset = GetQueryInCreate(self.get_queryset,query_par)     

        serializer = TaskSerializer( data = request.data ) 

        return ValidationCheck(serializer, day_tasks = queryset , user_random = None , random = False)
            

    def get_queryset(self,date,if_not_create=False,start=False):
        return DayTasks.objects.get_day(self.request.user,date,if_not_create,start)        


    def get_query_parameter(self):
        return self.request.query_params
  
    # Delete and update are in abstraction



@api_view(['DELETE'])
def DayDelete(request,pk=None):
    
    queryset = get_object_or_404(DayTasks,pk=pk,user=request.user)
    queryset.delete()
    return Response(status=status.HTTP_200_OK)



class RandomTasksView(TasksView):       # Random-tasks endpoint

    permission_classes = [
        IsAuthenticated
    ]


    def list(self,request):

        queryset = self.get_queryset()

        data_RESPONSE = {

            "Day" : None,       # No day related 
            "Tasks" : TaskSerializer(
                queryset,
                many=True,
                fields=("id","text","completed")
                ).data
        }

        return Response(data_RESPONSE)


    def create(self,request):
        
        serializer = TaskSerializer( data = request.data )
        return ValidationCheck(serializer, day_tasks = None , user_random = request.user  , random = True)


    def get_queryset(self):
        return self.request.user.tasks.all()        # Getting all random tasks related to user

        



