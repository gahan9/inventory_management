# coding=utf-8
__author__ = "Gahan Saraiya"
import nested_admin

from .models import *


class EffectiveCostInline(nested_admin.NestedTabularInline):
    model = EffectiveCost


class PurchaseRecordInline(nested_admin.NestedTabularInline):
    model = PurchaseRecord
