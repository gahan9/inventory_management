# coding=utf-8
from django.contrib import admin
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
    list_display = ["id", "cost", "discount", "effective_cost"]


class PurchaseRecordAdmin(admin.ModelAdmin):
    search_fields = ["name", "address"]
    list_display = ["id", "invoice_id", "purchased_from", "purchase_date", "delivery_date",
                    "payment_mode", "paid",
                    ]


admin.site.register(PurchaseCompany, PurchaseCompanyAdmin)
admin.site.register(EffectiveCost, EffectiveCostAdmin)
admin.site.register(ProductRecord, ProductRecordAdmin)
admin.site.register(PurchaseRecord, PurchaseRecordAdmin)

admin.site.site_header = 'Inventory administration'
admin.site.site_title = 'Inventory administration'
admin.site.index_title = 'Inventory administration'
