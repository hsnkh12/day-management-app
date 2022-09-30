from django.db import models
from django.conf import settings
from .managers import GoalsManager

class Goal(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null = True,
        related_name="goals"
        )

    title = models.CharField(
        max_length=25
        )

    work_started = models.CharField(
        max_length=10,
        null=True,
   
        )

    target_hours = models.PositiveIntegerField(
        default=0,
        help_text = "Maximum target hours is 20",
   
        )

    time_left = models.TimeField(
        null=True,
   
        )

    is_achieved = models.BooleanField(
        default=False
        )

    objects = GoalsManager()

    def __str__(self):
        return f"Title : {self.title}  -  Work started : {self.work_started}  -  Time left : {str(self.time_left)}"



class Work(models.Model):

    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        null=True,
        related_name="works"
        )

    time_spent = models.TimeField(
        null=True,

        )

    date = models.DateField(
        null=True,
        blank=True
        )

    def __str__(self):
        return f"Time spent : {str(self.time_spent)}  -  Date : {str(self.date)}"