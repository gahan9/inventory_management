# coding=utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from rest_framework import viewsets

from inventory_management.serializers import *

__author__ = "Gahan Saraiya"


class EffectiveCostViewSet(viewsets.ModelViewSet):
    serializer_class = EffectiveCostSerializer
    queryset = EffectiveCost.objects.all()


class PurchaseRecordViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseRecordSerializer
    queryset = PurchaseRecord.objects.all()


class DistributorViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseRecordSerializer
    queryset = PurchaseRecord.objects.all()


class HomePageView(LoginRequiredMixin, TemplateView):
    """
    Home page view
    """
    login_url = reverse_lazy('login')
    template_name = "home.html"
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context
