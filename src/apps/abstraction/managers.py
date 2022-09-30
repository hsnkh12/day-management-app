from django.db import models
from django.utils import timezone
from django.shortcuts import get_object_or_404


class DayManager(models.Manager):


    def get_day(self,   user,  date,   if_not_create=False,  start=False):
        
        if if_not_create == True or if_not_create == "True":
            
            queryset = self.select_related("user").filter(user=user,date=date)

            if queryset.exists():
                queryset = queryset.last()
                queryset.started = start
                queryset.save()

            else:
                queryset = self.create(date=date,user=user,started=start)

            return queryset

        else:
            
            return get_object_or_404(self, user=user,date=date )


    def get_days_related(self,user):
        return self.select_related("user").filter(user=user)

