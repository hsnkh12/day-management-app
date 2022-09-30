from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

from rest_framework.authtoken.models import Token




class User(AbstractUser):
    
    wallet_money = models.DecimalField(
        default=100,
        max_digits = 7,
        decimal_places=2,
        )

    weight = models.DecimalField(
        default=0,
        max_digits = 3,
        decimal_places=2,
        )

    def __str__(self):
        return self.username



@receiver(post_save , sender = User)
def create_auth_token(sender , instance = None , created = False , **kwargs):
    if created:
        Token.objects.create(user=instance)