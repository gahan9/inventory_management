# coding=utf-8
from easy_select2.utils import select2_modelform
from nested_inline.admin import NestedModelAdmin

__author__ = "Gahan Saraiya"
from django.contrib import admin

from core_settings.settings import COMPANY_TITLE
from .admin_inlines import *

# PurchaseCompanyForm = select2_modelform(PurchaseCompany, {'width': "600px"})
# BaseProductRecordForm = select2_modelform(BaseProductRecord, {'width': "600px"})
# PurchaseRecordForm = select2_modelform(BaseProductRecord, {'width': "600px"})
# BaseEffectiveCostForm = select2_modelform(BaseEffectiveCost, {'width': "300px"})


class BaseDistributorAdmin(NestedModelAdmin):
    inlines = [PurchaseRecordInline]
    search_fields = ["name", "address"]
    list_display = ["id", "name", "contact_number", "alternate_contact_number", "fax_number", "address"
                    ]


class ProductRecordAdmin(NestedModelAdmin):
    inlines = [EffectiveCostInline]
    search_fields = ["name", "launched_by"]
    list_display = ["id", "name", "price", "product_launch_date", "launched_by",
                    "version",
                    ]


class BaseEffectiveCostAdmin(admin.ModelAdmin):
    # form = BaseEffectiveCostForm
    search_fields = ["discount"]
    list_display = ["id", "cost", "discount", "effective_cost", "total_effective_cost"]
    readonly_fields = ["effective_cost", "total_effective_cost"]


class BasePurchaseRecordAdmin(admin.ModelAdmin):
    search_fields = ["name", "address"]
    list_display = ["id", "invoice_id", "purchased_from", "purchase_date", "get_items",
                    "total_amount", "payment_mode", "payment_status"
                    ]
    readonly_fields = ["total_amount"]
    fieldsets = (
        (None, {'fields': ["invoice_id"]}),
        ("Items", {'fields': ["items"]}),
        ("Payment Details", {'fields': ["total_amount", "payment_mode", "payment_status"]}),
        ("Other Details", {'fields': ["purchased_from", "purchase_date"]}),
    )
    add_fieldsets = (
        (None, {'fields': ["invoice_id"]}),
        ("Items", {'fields': ["items"]}),
        ("Payment Details", {'fields': ["total_amount", "payment_mode", "payment_status"]}),
        ("Other Details", {'fields': ["purchased_from", "purchase_date"]}),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


admin.site.site_header = COMPANY_TITLE + ' administration'
admin.site.site_title = COMPANY_TITLE + ' administration'
admin.site.index_title = COMPANY_TITLE + ' administration'
