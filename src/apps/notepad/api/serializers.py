from rest_framework import serializers
from ..models import *
from ...abstraction.serializers import DynamicFieldsModelSerializer




class NoteSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Note
        fields = '__all__'
        read_only_field = ["id"]