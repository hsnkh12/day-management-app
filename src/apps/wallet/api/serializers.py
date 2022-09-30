from rest_framework import serializers
from ..models import *
from ...abstraction.serializers import DynamicFieldsModelSerializer


class DaySpendEarnSerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = DaySpendingsEarnings
        fields = '__all__'


class SpendingSerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = Spending
        fields = '__all__'

    def save(self,*args,**kwargs):

        
        part_of_plan = kwargs["part_of_plan"]

        if not part_of_plan :
            day = kwargs["day_spend_earn"]
            user = day.user
            amount = self.validated_data["amount"]

            day.total_spent+=amount

            if amount > user.wallet_money:
                raise serializers.ValidationError({
                    "Error":"You do not have enough money"
                })

            user.wallet_money-=amount
            
            day.save()
            user.save()

        

        super().save(*args, **kwargs)




class EarningSerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = Earning
        fields = '__all__'

    def save(self,*args,**kwargs):

        day = kwargs["day_spend_earn"]
        user = day.user
        amount = self.validated_data["amount"]

        day.total_earned+=amount
        user.wallet_money+=amount
        
        day.save()
        user.save()

        super().save(*args, **kwargs)


class PlanSpendSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = PlanSpendings
        fields = '__all__'