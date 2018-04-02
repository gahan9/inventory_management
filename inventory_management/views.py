# coding=utf-8
__author__ = "Gahan Saraiya"
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from rest_framework import viewsets

from core_settings.settings import COMPANY_TITLE
from inventory_management.models import PurchaseRecord
from inventory_management.serializers import PurchaseRecordSerializer


class PurchaseRecordViewSet(viewsets.ModelViewSet):
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
