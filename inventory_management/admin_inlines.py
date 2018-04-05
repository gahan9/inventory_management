# coding=utf-8
__author__ = "Gahan Saraiya"

from django.contrib.admin.options import TabularInline
from nested_inline.admin import NestedStackedInline
from .models import *


class EffectiveCostInline(NestedStackedInline):
    model = EffectiveCost
    extra = 0


class PurchaseRecordInline(NestedStackedInline):
    model = PurchaseRecord
    extra = 0
