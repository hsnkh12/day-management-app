from django.shortcuts import (
    get_object_or_404
    )
from rest_framework import status
from rest_framework.response import Response
from .serializers import (
    SpendingSerializer,
    EarningSerializer,
    DaySpendEarnSerializer,
    PlanSpendSerializer
    )
from ..models import (
    DaySpendingsEarnings,
    Spending,
    Earning,
    PlanSpendings
    )

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from ...abstraction.utils import (
    ValidationCheck,
    ValidateDate,
    CheckQueryParm,GetDay,GetQueryInCreate)
from ...abstraction.premissions import UserPrem


class DaySpendingsEarningsView(ViewSet):        # day-spendings-earnings endpoint, to manage days and spends and earns


    permission_classes = [
        IsAuthenticated
    ]


    def list(self,request):

        query_par = self.get_query_parameter() 
        date = CheckQueryParm(query_par,"date",other=False)     # Getting the date wanted


        if date:       # It means that we are triggering a specific day wether in calander or other

            ValidateDate(date)      # Checking it the date is in the right format
            data = GetDay(self.get_queryset, query_par, date, app="wallet")

            data_RESPONSE = {
            
                "Wallet" : request.user.wallet_money,

                "Day" : DaySpendEarnSerializer(
                    data['day'],
                    ).data,

                "Spendings" : SpendingSerializer(
                    data['spendings'],
                    many=True,
                    fields=("id","amount","more_details","priority")
                    ).data,

                "Earnings" : SpendingSerializer(
                    data['earnings'],
                    many=True,
                    fields=("id","amount","more_details")
                    ).data
            }

        else:       # No specidic day (list of days)
            
            queryset = DaySpendingsEarnings.objects.get_days_related(request.user).order_by("date")
            data_RESPONSE = {
                "Days" : DaySpendEarnSerializer(
                    queryset,
                    fields=("id","date","expired","total_spent","total_earned"),
                    many=True
                    ).data
            }
        
        return Response(data_RESPONSE)


    def create(self,request):

        query_par = self.get_query_parameter()
        queryset = GetQueryInCreate(self.get_queryset,query_par) 
        type_ = query_par['type']
        kwargs = {'day_spend_earn':queryset}

        
        
        if type_ == "spending":

            serializer = SpendingSerializer(data = request.data)
            kwargs.update({'part_of_plan':False})

        else:

            serializer = EarningSerializer(data = request.data)


        return ValidationCheck(serializer,**kwargs)


    def destroy(self,request,pk=None):

        query_par = self.get_query_parameter()

        type_ = CheckQueryParm(query_par,"type")
        
        if type_ == "spending":

            queryset = get_object_or_404(Spending, pk=pk)
            

        else:

            queryset = get_object_or_404(Earning, pk=pk)

        queryset.delete()
        return Response(status=status.HTTP_200_OK)


    def get_queryset(self,date,if_not_create=False,start=False):
        return DaySpendingsEarnings.objects.get_day(self.request.user,date,if_not_create,start)


    def get_query_parameter(self):
        return self.request.query_params



@api_view(['DELETE'])
def DayDelete(request,pk=None):
    
    queryset = get_object_or_404(DaySpendingsEarnings,pk=pk,user=request.user)
    queryset.delete()
    return Response(status=status.HTTP_200_OK)



class SpendingsPlanView(ViewSet):       # spendings-plan endpoint to manage plans


    permission_classes = [
        IsAuthenticated,
    ]


    def list(self,request):

        queryset = self.get_queryset()
        
        data_RESPONSE = {

            "Plans" : PlanSpendSerializer(
                queryset,
                many=True,
                fields=("id","title","Type")
            ).data
        }

        return Response(data_RESPONSE)


    def retrieve(self, request, pk=None):
        
        queryset = get_object_or_404(PlanSpendings, pk=pk, user = request.user)
        spendings = queryset.spendings.all()

        data_RESPONSE = {

            "Plan" : PlanSpendSerializer(
                queryset,
            ).data,

            "Spendings" : SpendingSerializer(
                spendings,
                many=True,
                fields=("id","day_number","amount","more_details")
            ).data,
        }

        return Response(data_RESPONSE)


    def create(self,request):
        
        serializer = PlanSpendSerializer(data = request.data ,user = request.user)
        return ValidationCheck(serializer,user=request.user)


    def destroy(self,request, pk=None):

        queryset = get_object_or_404(PlanSpendings, pk=pk,user = request.user)
        queryset.delete()

        return Response(status=status.HTTP_200_OK)


    def get_queryset(self):
        return PlanSpendings.objects.get_related_plans(self.request.user)



class SpendingsPlanDetailView(APIView):     # spendings-plan-detail enpoint to manage only spendings

    permission_classes = [
        IsAuthenticated
    ]

    def post(self,request, pk=None):

        queryset = get_object_or_404(PlanSpendings, pk=pk ,user = request.user)
        serializer = SpendingSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(day_spend_earn=None,part_of_plan=True)
            queryset.spendings.add(serializer.data["id"])
            queryset.save()

            return Response(serializer.data)

        return Response(serializer.errors)


    def delete(self,request, pk=None):
        
        queryset = get_object_or_404(Spending, pk=pk)
        queryset.delete()

        return Response(status=status.HTTP_200_OK)




