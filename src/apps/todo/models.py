from django.db import models
from django.conf import settings
from ..abstraction.managers import DayManager
from ..abstraction.models_ import (
    AbstractDay,
)
from rest_framework.response import Response


class DayTasks(AbstractDay):

    rate = models.DecimalField(
        default = 0,
        max_digits = 2,
        decimal_places=1,
    )

    objects = DayManager()

    class Meta:
        verbose_name = "Day Tasks"
        verbose_name_plural = "Days Tasks"

    def __str__(self):
        return f" Date : {str(self.date)}  -  Rate : {str(self.rate)}  -  Expired : {self.expired}"

       

class Task(models.Model):
    
    day_tasks = models.ForeignKey(
        DayTasks,
        null=True,
        related_name="tasks",
        on_delete = models.CASCADE,
        verbose_name="Day tasks"
        )

    # If task is random
    user_random = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        help_text= "If task is random",
        verbose_name="Random task for user",
        on_delete = models.CASCADE,
        related_name="tasks",
    )

    text = models.CharField(
        max_length=50,
        verbose_name="Task"
        )

    time = models.TimeField(
        blank=True,
        null=True,
        help_text="Optional"
        )

    important = models.BooleanField(
        default=False,
        )

    completed = models.BooleanField(
        default=False,
        )

    random = models.BooleanField(
        default=False,
        )

    def __str__(self):
        return f" Time : {str(self.time)}  -  Random : {self.random}  -  Completed : {self.completed}"