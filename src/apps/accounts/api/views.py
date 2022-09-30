from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import registrationSerializer,ProfileSerializer
from ..models import User,Token
from rest_framework.views import APIView 
from rest_framework.viewsets import ViewSet
import json
from rest_framework.generics import RetrieveUpdateAPIView

@api_view(['POST'])
def registerView(request):

    serial = registrationSerializer(data = request.data)

    if serial.is_valid():

        new_user  = serial.save()
        token = Token.objects.get(user=new_user).key

        data = {"Token":token, "User":serial.data}
        return Response(data)
    
    return Response(serial.errors)

        
        


class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)



class ProfileView(RetrieveUpdateAPIView):

    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user



class Contact(APIView):

    def post(self,request,format=None):
        pass