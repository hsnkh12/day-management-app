from django.db import models
from django.conf import settings

class AbstractDay(models.Model):

    date = models.DateField(
        blank=True,
        null=True,
        )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete = models.CASCADE,
        )

    started = models.BooleanField(
        default=False
        )

    expired = models.BooleanField(
        default=False
        )

    class Meta:
        abstract = True


class spendingEarningAbstract(models.Model):

    amount = models.DecimalField(
        max_digits = 10,
        decimal_places=2,
    )

    more_details = models.CharField(
        max_length=75,
        blank=True,
        verbose_name = "More details",
        help_text = "Optional",
    )

    class Meta:
        abstract = True