# coding=utf-8
from rest_framework import serializers

from inventory_management.models import PurchaseRecord


class PurchaseRecordSerializer(serializers.HyperlinkedModelSerializer):
    final_amount = serializers.SerializerMethodField()

    def update(self, instance, validated_data):
        instance = super(PurchaseRecordSerializer, self).update(instance, validated_data)
        val = sum([product['total_effective_cost'] for product in instance.items.values()])
        return val

    def get_final_amount(self, obj):
        val = sum([product['total_effective_cost'] for product in obj.items.values()])
        return val

    class Meta:
        model = PurchaseRecord
        fields = ["invoice_id", "purchase_date",
                  "purchased_from", "purchase_date", "delivery_date",
                  "items", "payment_mode", "payment_status",
                  "total_amount", "final_amount"]
        # fields = "__all__"


class EffectiveCostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PurchaseRecord
        fields = "__all__"
