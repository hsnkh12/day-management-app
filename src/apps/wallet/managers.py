from django.db import models
from django.utils import timezone



class PlanSpendManager(models.Manager):

    def get_related_plans(self,user):
        return self.select_related("user").filter(user=user)

    def get_related_spendings(self):
        return self.spendings.objects.all()