# coding=utf-8
from django.contrib import admin

from core_settings.settings import COMPANY_TITLE
from inventory_management.models import *


class PurchaseCompanyAdmin(admin.ModelAdmin):
    search_fields = ["name", "address"]
    list_display = ["id", "name", "contact_number", "alternate_contact_number", "fax_number",
                    "address",
                    ]


class ProductRecordAdmin(admin.ModelAdmin):
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
    list_display = ["id", "invoice_id", "purchased_from", "purchase_date", "delivery_date",
                    "total_invoice_amount", "payment_mode", "paid"
                    ]
    readonly_fields = ["total_amount", "paid"]

    def total_invoice_amount(self, obj):
        val = sum([product['total_effective_cost'] for product in obj.items.values()])
        # print([product.total_effective_cost for product in obj.items.iterator()])
        # print(val)
        return val


admin.site.register(PurchaseCompany, PurchaseCompanyAdmin)
admin.site.register(EffectiveCost, EffectiveCostAdmin)
admin.site.register(ProductRecord, ProductRecordAdmin)
admin.site.register(PurchaseRecord, PurchaseRecordAdmin)

admin.site.site_header = COMPANY_TITLE + ' administration'
admin.site.site_title = COMPANY_TITLE + ' administration'
admin.site.index_title = COMPANY_TITLE + ' administration'
