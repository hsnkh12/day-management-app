from django.db import models


class GoalsManager(models.Manager):

    def get_related_gaols(self,user):
        
        return self.select_related("user").filter(user=user)