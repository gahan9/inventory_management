# coding=utf-8
from django.contrib.admin.options import TabularInline

__author__ = "Gahan Saraiya"
from nested_inline.admin import NestedStackedInline
from .models import *


class EffectiveCostInline(NestedStackedInline):
    model = EffectiveCost
    extra = 0


class PurchaseRecordInline(NestedStackedInline):
    model = PurchaseRecord
    extra = 0
