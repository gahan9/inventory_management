# coding=utf-8
from rest_framework import serializers

from inventory_management.models import PurchaseRecord


class PurchaseRecordSerializer(serializers.ModelSerializer):
    final_amount = serializers.SerializerMethodField()

    def update(self, instance, validated_data):
        instance = super(PurchaseRecordSerializer, self).update(instance, validated_data)
        if instance.payment_mode:
            instance.paid = True
        else:
            instance.paid = False
        val = sum([product['total_effective_cost'] for product in instance.items.values()])
        return val

    def get_final_amount(self, obj):
        val = sum([product['total_effective_cost'] for product in obj.items.values()])
        return val

    class Meta:
        model = PurchaseRecord
        fields = ["invoice_id", "purchase_date", "total_amount", "paid", "final_amount"]


class EffectiveCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseRecord
        fields = "__all__"
