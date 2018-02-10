from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from inventory_management.models import PurchaseRecord
from inventory_management.serializers import PurchaseRecordSerializer


class PurchaseRecordViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseRecordSerializer
    queryset = PurchaseRecord.objects.all()
