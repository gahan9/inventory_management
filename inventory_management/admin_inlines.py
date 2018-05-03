# coding=utf-8
from django.contrib.admin.options import TabularInline
from nested_inline.admin import NestedStackedInline
from .models import *

__author__ = "Gahan Saraiya"

__all__ = ['EffectiveCostInline', 'PurchaseRecordInline']


class EffectiveCostInline(NestedStackedInline):
    model = EffectiveCost
    extra = 0


class PurchaseRecordInline(NestedStackedInline):
    model = PurchaseRecord
    extra = 0
