# coding=utf-8
from rest_framework import serializers

from inventory_management.models import *


class PurchaseRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PurchaseRecord
        fields = ["invoice_id", "purchase_date",
                  "purchased_from", "purchase_date", "delivery_date",
                  "items", "payment_mode", "payment_status",
                  "total_amount"]
        # fields = "__all__"


class EffectiveCostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EffectiveCost
        fields = "__all__"


class DistributorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Distributor
        fields = "__all__"
