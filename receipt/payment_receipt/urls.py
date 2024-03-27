from django.urls import path

from .views import CashMachineAPIView

urlpatterns = [
    path('', CashMachineAPIView.as_view(), name='cashmachine'),
]
