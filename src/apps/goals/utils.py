from rest_framework.response import Response
from rest_framework import status,response
from ..abstraction.utils import (
    ValidationCheck,
    ValidateDate,)
import math
import datetime

def EndTheWork(queryset,seconds_spent,seconds_left):
    
    if queryset.work_started == "" or not queryset.work_started :     # Checking if the work is not started
        raise serializers.ValidationError({
            "Error" : "Start the work to end it"
        })

    queryset.work_started = None

    if seconds_spent>=seconds_left:     # Checking if time spent bigger than left
                
        queryset.time_left = "00:00:00"
        queryset.is_achieved = True
        seconds_spent -= seconds_left
            
    else:

        seconds_left-=seconds_spent     # Calculate the time deff between time left and spent
        queryset.time_left = ConvertSecondsToTime(seconds_left)

    queryset.save()
    return seconds_spent



def ConvertTimeToSeconds(time):
    
    h = math.floor(time[0]*60*60)
    m = math.floor(time[1]*60)
    s = time[2]

    return h + m + s



def ConvertSecondsToTime(seconds):

    time = str(datetime.timedelta(seconds=seconds))
    point = time.index(":")

    h = time[point-2:point]
    if h == "": h = time[point-1:point]

    m = time[point+1:point+3]
    s = time[point+4:point+6]

    return time
