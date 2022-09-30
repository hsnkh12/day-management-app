from django.db import models
from django.conf import settings
from ..abstraction.managers import DayManager
from ..abstraction.models_ import (
    AbstractDay,
)


class DayCalories(AbstractDay):

    total_calories = models.PositiveIntegerField(
        default = 0,
        verbose_name="Total calories"
    )

    objects = DayManager()

    class Meta:
        verbose_name = "Day calories"
        verbose_name_plural = "Days calories"

    def __str__(self):
        return f"Date : {str(self.date)}  -  Total calories : {str(self.total_calories)}  -  Expired : {self.expired}"
    


class Food(models.Model):

    CHOICES = (
        ("Breakfast","Breakfast"),
        ("Lunch","Lunch"),
        ("Dinner","Dinner"),
        ("Snack","Snack")
    )

    foodId = models.TextField(
        
    )

    day_calories = models.ForeignKey(
        DayCalories,
        null=True,
        verbose_name = "Related day",
        related_name="foods",
        on_delete = models.CASCADE
    )

    name = models.CharField(
        max_length=75,
    )

    time = models.CharField(
        max_length=10,
        choices=CHOICES
    )

    grams = models.PositiveIntegerField(
        default = 0,
    )

    calories = models.PositiveIntegerField(
        default = 0,
        verbose_name="Calories"
    )


    def delete(self,*args,**kwargs):

        day = self.day_calories
        day.total_calories-= self.calories
        day.save()

        super(Food, self).delete(*args, **kwargs)

    def __str__(self):
        return f"Name : {self.name}  -  Time : {self.time}  -  Calories : {str(self.calories)}"

    
