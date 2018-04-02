# coding=utf-8
__author__ = "Gahan Saraiya"
from django.contrib import admin

from core_settings.settings import COMPANY_TITLE
from .admin_inlines import *


class PurchaseCompanyAdmin(admin.ModelAdmin):
    inlines = [PurchaseRecordInline]
    search_fields = ["name", "address"]
    list_display = ["id", "name", "contact_number", "alternate_contact_number", "fax_number",
                    "address",
                    ]


class ProductRecordAdmin(nested_admin.NestedModelAdmin):
    inlines = [EffectiveCostInline]
    search_fields = ["name", "launched_by"]
    list_display = ["id", "name", "price", "product_launch_date", "launched_by",
                    "version",
                    ]


class EffectiveCostAdmin(admin.ModelAdmin):
    search_fields = ["discount"]
    list_display = ["id", "cost", "discount", "effective_cost", "total_effective_cost"]
    readonly_fields = ["effective_cost", "total_effective_cost"]


class PurchaseRecordAdmin(admin.ModelAdmin):
    search_fields = ["name", "address"]
    list_display = ["id", "invoice_id", "purchased_from", "purchase_date", "get_items",
                    # "delivery_date",
                    "total_amount", "payment_mode", "payment_status"
                    ]
    readonly_fields = ["total_amount", "payment_status"]


admin.site.register(PurchaseCompany, PurchaseCompanyAdmin)
admin.site.register(EffectiveCost, EffectiveCostAdmin)
admin.site.register(ProductRecord, ProductRecordAdmin)
admin.site.register(PurchaseRecord, PurchaseRecordAdmin)

admin.site.site_header = COMPANY_TITLE + ' administration'
admin.site.site_title = COMPANY_TITLE + ' administration'
admin.site.index_title = COMPANY_TITLE + ' administration'
