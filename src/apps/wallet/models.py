from django.db import models
from django.conf import settings
from ..abstraction.managers import DayManager
from .managers import PlanSpendManager
from ..abstraction.models_ import (
    AbstractDay,
    spendingEarningAbstract
)





# Models

class DaySpendingsEarnings(AbstractDay):
    
    total_spent = models.DecimalField(
        default=0,
        max_digits = 7,
        decimal_places=2,
        verbose_name="Total spent"
    )

    total_earned = models.DecimalField(
        default=0,
        max_digits = 7,
        decimal_places=2,
        verbose_name="Total earned"
    )

    objects = DayManager()

    class Meta:
        verbose_name = "Day spendings and earnings"
        verbose_name_plural = "Days spendings and earnings"

    def __str__(self):
        return f" Date : {str(self.date)}  -  Total spent : {str(self.total_spent)}  -  Total earned : {str(self.total_earned)}  -  Expired : {self.expired}"

    def apply_money_changes(self):
        pass
        
    

class Spending(spendingEarningAbstract):

    day_spend_earn = models.ForeignKey(
        DaySpendingsEarnings,
        null=True,
        blank=True,
        on_delete = models.CASCADE,
        verbose_name="Day spendings and earnings",
        related_name="spendings"
    )

    part_of_plan = models.BooleanField(
        default = False,
        verbose_name="Part of a plan"
    )

    day_number = models.PositiveIntegerField(
        default = 0,
        verbose_name = "Day number ( plan )",
        help_text = "Plan required"
    )

    priority = models.BooleanField(
        default=False
    )

    type_ = "spending"

    def __str__(self):
        return f" Amount : {str(self.amount)}  -  Plan : {self.part_of_plan}"
    

    def delete(self,*args,**kwargs): 

        if not self.part_of_plan:
            
            day = self.day_spend_earn
            user = day.user
            day.total_spent-=self.amount
            user.wallet_money+=self.amount
            day.save()
            user.save()

        super(Spending, self).delete(*args, **kwargs)
    



class Earning(spendingEarningAbstract):

    day_spend_earn = models.ForeignKey(
        DaySpendingsEarnings,
        null=True,
        on_delete = models.CASCADE,
        verbose_name="Day spendings and earnings",
        related_name="earnings"
    )

    type_ = "earning"

    def __str__(self):
        return f" Amount : {str(self.amount)}"
    

    def delete(self,*args,**kwargs):

        day = self.day_spend_earn
        user = day.user
        day.total_earned-=self.amount
        user.wallet_money-=self.amount
        day.save()
        user.save()

        super(Earning, self).delete(*args, **kwargs)

    


class PlanSpendings(models.Model):

    CHOICES = (
        ("Weekly","Weekly"),
        ("Monthly","Monthly")
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete = models.CASCADE,
        )

    spendings = models.ManyToManyField(
        Spending,
        blank=True,
    )

    title = models.CharField(
        max_length=25,
    )

    Type = models.CharField(
        max_length=8,
        choices=CHOICES,
        verbose_name="Plan Type"
    )

    objects = PlanSpendManager()

    class Meta:
        verbose_name = "Spending plan"
        verbose_name_plural = "Spending plans"

    def __str__(self):
        return f" Type : {self.Type}  -  Title : {self.title}"

    @property
    def total_budget_needed(self):
        return [x.amount for x in self.spendings.all()]






