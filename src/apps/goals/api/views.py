from django.shortcuts import (
    get_object_or_404
    )

from rest_framework import serializers

from ...abstraction.utils import (
    ValidationCheck,
)
from ..utils import (EndTheWork, ConvertSecondsToTime,
    ConvertTimeToSeconds,)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GoalSerializer,WorkSerializer
from ..models import Goal,Work
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import (
    IsAuthenticated,
    )


class GoalView(ViewSet):        # goal-works endpoint

    permission_classes = [
        IsAuthenticated
    ]


    def list(self,request):     # Get lit of goals related to user

        queryset = self.get_queryset()

        data_RESPONSE = {
            "Goals":GoalSerializer(
                queryset,
                many=True,
                fields=("id","title","time_left","work_started","target_hours")
            ).data
        }

        return Response(data_RESPONSE)


    def retrieve(self,request,pk=None):     # Get specific goal

        queryset = get_object_or_404(Goal,pk=pk, user=request.user)
        works = Work.objects.select_related("goal").filter(goal=queryset)       # Works related

        data_RESPONSE = {

            "Goal":GoalSerializer(
                queryset,
            ).data,

            "Works":WorkSerializer(
                works,
                many=True,
                fields=("id","time_spent","date")
            ).data
        }

        return Response(data_RESPONSE)


    def create(self,request):       # Creat new goal
        
        serializer = GoalSerializer(data=request.data)
        hours = request.data["target_hours"]

        if int(hours) < 10:   time = f"0{hours}:00:00"
        else:  time = f"{hours}:00:00"

        return ValidationCheck(serializer, user=request.user,time_left = time)


    def destroy(self,request,pk=None):
        
        queryset = get_object_or_404(Goal,pk=pk,user=request.user)
        queryset.delete()

        return Response(status=status.HTTP_200_OK)


    def update(self,request,pk=None):

        query_par = request.query_params
        queryset = get_object_or_404(Goal,pk=pk,user=request.user)

        if not query_par:       # Action is not defined
            raise serializers.ValidationError({
                "Error":"Action required"
            })


        if query_par["action"] == "start":      # Start the work in this goal

            if queryset.is_achieved:
                raise serializers.ValidationError({ "Erorr" : "This goal is achieved"})
                

            queryset.work_started = query_par["time_started"]
            new_work = None
            queryset.save()


        elif query_par["action"] == "end":      # End the work in this goal
            
            time_left = queryset.time_left 

            seconds_left = ConvertTimeToSeconds((time_left.hour,time_left.minute,time_left.second))
            seconds_spent = int(query_par["spent"])

            if seconds_spent>72000:     # Hours are bigger than 20 hours
                raise serializers.ValidationError({
                "Error":"20 hours is max"
            })


            seconds_spent = EndTheWork(queryset,seconds_spent,seconds_left)     # Ending the work by calcuation the deff between time spent and time left

            work = Work.objects.create(     # Creating new work based on the time spent and date
                goal=queryset,
                time_spent= ConvertSecondsToTime(seconds_spent),
                date = timezone.now().date()
            )
            new_work = WorkSerializer(work).data
            

        data_RESPONSE = {

            "Goal":GoalSerializer(
                queryset,
            ).data,

            "Work":new_work
        }

        return Response(data_RESPONSE)

        
    def get_queryset(self):
        return Goal.objects.get_related_gaols(self.request.user)
    


@api_view(["DELETE"])
def deleteWork(request,pk):

    queryset = get_object_or_404(Work,pk=pk)
    queryset.delete()

    return Response(status=status.HTTP_200_OK)
