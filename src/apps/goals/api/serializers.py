from rest_framework import serializers
from ..models import *
from ...abstraction.serializers import DynamicFieldsModelSerializer


class GoalSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_field = ["id"]

    def validate(self,data):

        hours = data["target_hours"]

        if hours<0 or hours >20:
            raise serializers.ValidationError({
                "Error" : "20 hours is max"
            })

        return data


class WorkSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Work
        fields = '__all__'
