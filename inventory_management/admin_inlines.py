# coding=utf-8
import nested_admin

from .models import *


class EffectiveCostInline(nested_admin.NestedTabularInline):
    model = EffectiveCost


class PurchaseRecordInline(nested_admin.NestedTabularInline):
    model = PurchaseRecord
