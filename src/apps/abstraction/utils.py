from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import (
    get_object_or_404
    )
from rest_framework import status,response

from rest_framework.decorators import api_view
from rest_framework import serializers

import datetime

def ValidateDate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except:
        raise serializers.ValidationError({"Error":"Incorrect data format, should be YYYY-MM-DD"})



def ValidationCheck(serializer,**kwargs):
    
    if serializer.is_valid():

            serializer.save(**kwargs)
            return Response(serializer.data)

    return Response(serializer.errors)



def CheckQueryParm(query_par,key,other=None):

    error = serializers.ValidationError({"Error":f" '{key}' parameter is required"})

    try:
        key = query_par[key]

        if not key:

            if other is not None:
                return other
            raise error

        return key

    except:
        if other is not None:
            return other
        raise error





def GetDay( queryset, query_par, date, app="todo"):

    if_not_create = CheckQueryParm(query_par,"if_not_create",other=False)       # Bool object to know that if we don't find this object, we can creat new one directly
    start = CheckQueryParm(query_par,"start",other=False)       # Bool object to know if we want to create a new day to start it or not yet
    day = queryset(date,if_not_create,start)

    data = { 'day' : day }

    if app == "todo":

        tasks = day.tasks.select_related("day_tasks").all().order_by("time")
        data.update( { 'tasks' : tasks } )

    elif app == "wallet":

        spendings = day.spendings.select_related("day_spend_earn").all()
        earnings = day.earnings.select_related("day_spend_earn").all()

        data.update( { 'spendings' : spendings , 'earnings' : earnings  } )

    else:
        foods = day.foods.select_related('day_calories').all()
        data.update( { 'foods' : foods  } )

    
    return data





def GetQueryInCreate( queryset, query_par ):

    date = CheckQueryParm(query_par,"date")
    if_not_create = CheckQueryParm(query_par,"if_not_create",other=False)       # bcs maybe the user is creating task in the future
    ValidateDate(date)

    return queryset(date,if_not_create)





