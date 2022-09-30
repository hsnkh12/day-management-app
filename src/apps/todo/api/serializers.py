from rest_framework import serializers
from ..models import *
from ...abstraction.serializers import DynamicFieldsModelSerializer



class DayTasksSerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = DayTasks
        fields = '__all__'



class TaskSerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = Task
        fields = '__all__'

