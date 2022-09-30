from rest_framework import serializers
from ..models import *
from ...abstraction.serializers import DynamicFieldsModelSerializer


class DayCaloriesSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = DayCalories
        fields = '__all__'



class FoodSerializer(DynamicFieldsModelSerializer):


    class Meta:
        model = Food
        fields = '__all__'


    def save(self,*args,**kwargs):

        day = kwargs["day_calories"]

        day.total_calories+= self.validated_data["calories"]
        day.save()

        super().save(*args, **kwargs)