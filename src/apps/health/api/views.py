from django.shortcuts import (
    get_object_or_404
    )
from rest_framework import status
from rest_framework.response import Response

from .serializers import (
    DayCaloriesSerializer,
    FoodSerializer
    )

from ..models import (
    DayCalories,
    Food
    )

from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated

from ...abstraction.utils import (
    ValidationCheck,
    ValidateDate,
    CheckQueryParm,GetDay,GetQueryInCreate)

from rest_framework.decorators import api_view


class DayCaloriesView(ViewSet):

    permission_classes = [
        IsAuthenticated
    ]
    
    def list(self,request):
        
        query_par = self.get_query_parameter() 
        date = CheckQueryParm(query_par,"date",other=False)     # Getting the date wanted

        if date:       # It means that we are triggering a specific day wether in calander or other

            ValidateDate(date)      # Checking it the date is in the right format
            data = GetDay(self.get_queryset, query_par, date, app="health")

            data_RESPONSE = {

                "Day" : DayCaloriesSerializer(
                    data['day'],
                ).data,

                "Foods" : FoodSerializer(
                    data['foods'],
                    many=True,
                ).data
            }

        else:       # No specidic day (list of days)

            queryset = DayCalories.objects.get_days_related(request.user).order_by("date")

            data_RESPONSE = {
                "Days" : DayCaloriesSerializer(
                    queryset,
                    fields=("id","date","total_calories","expired"),
                    many=True
                    ).data
            }

        return Response(data_RESPONSE)


    def create(self,request):

        query_par = self.get_query_parameter()
        queryset = GetQueryInCreate(self.get_queryset,query_par)     

        serializer = FoodSerializer(data=request.data)

        return ValidationCheck(serializer, day_calories = queryset)


    def destroy(self,request,pk=None):

        queryset = get_object_or_404(Food,pk=pk)

        if queryset.day_calories.user != request.user:
            Response(status=status.HTTP_401_UNAUTHORIZED)
            
        queryset.delete()
        
        return Response(status=status.HTTP_200_OK)
        

    def get_queryset(self,date,if_not_create=False,start=False):
        return DayCalories.objects.get_day(self.request.user,date,if_not_create,start)
    

    def get_query_parameter(self):
        return self.request.query_params


@api_view(['DELETE'])
def DayDelete(request,pk=None):
    
    queryset = get_object_or_404(DayCalories,pk=pk,user=request.user)
    queryset.delete()
    return Response(status=status.HTTP_200_OK)