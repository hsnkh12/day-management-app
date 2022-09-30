from django.urls import path,include
from .views import (
    DaySpendingsEarningsView,
    SpendingsPlanView,
    SpendingsPlanDetailView,
    DayDelete
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('day-spendings-earnings',DaySpendingsEarningsView,basename="day-spendings-earnings")
router.register('spending-plans',SpendingsPlanView,basename="spending-plans")


urlpatterns = [

    path("spending-plan-detail/<pk>/",SpendingsPlanDetailView.as_view(),name="spending-plan-detail"),
    path("day-spendings-earnings-delete/<pk>/",DayDelete)
    
]

urlpatterns += router.urls