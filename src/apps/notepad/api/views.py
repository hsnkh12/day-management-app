from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
    )
from django.utils import timezone
from ...abstraction.utils import ValidationCheck
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NoteSerializer
from ..models import Note
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from rest_framework.permissions import (
    IsAuthenticated,
    )



class NoteView(ViewSet):

    permission_classes = [
        IsAuthenticated
    ]


    def list(self,request):
        
        queryset = self.get_queryset()

        data_RESPONSE = {
            "Notes" : NoteSerializer(
                queryset,
                many=True,
                fields = ("id","title","date")
            ).data
        }

        return Response(data_RESPONSE)


    def retrieve(self,request,pk=None):
        
        queryset = get_object_or_404(Note,pk=pk,user=request.user)

        data_RESPONSE = {
            "Note" : NoteSerializer(
                queryset,
                fields = ("id","title","date","text")
            ).data
        }

        return Response(data_RESPONSE)


    def create(self,request):

        serializer = NoteSerializer(data=request.data)

        return ValidationCheck(serializer, date=timezone.now().date(),user=request.user)


    def update(self,request,pk=None):
        
        queryset = get_object_or_404(Note,pk=pk,user=request.user)
        serializer = NoteSerializer(queryset,data=request.data)

        return ValidationCheck(serializer, date=timezone.now().date(),user=request.user)


    def destroy(self,request,pk=None):
        
        queryset = get_object_or_404(Note,pk=pk,user=request.user)

        queryset.delete()
        return Response(status=status.HTTP_200_OK)


    def get_queryset(self):
        return Note.objects.get_relatd_notes(user=self.request.user)
    