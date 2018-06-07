from django.contrib import admin
from main.admin import *
from .models import *


class CustomerDetailAdmin(BaseCustomerDetailAdmin):
    pass


class SaleRecordAdmin(BaseSaleRecordAdmin):
    search_fields = ["name", "address"]
    list_display = ["id", "invoice_id", "purchase_date", "get_items",
                    "get_total", "payment_mode", "payment_status", "customer"
                    ]
    readonly_fields = ["get_total"]
    fieldsets = (
        (None, {'fields': ["invoice_id", "purchase_date"]}),
        ("Items", {'fields': ["items"]}),
        ("Payment Details", {'fields': ["get_total", "payment_mode", "payment_status"]}),
        ("Customer Details", {'fields': ["customer"]}),
    )
    add_fieldsets = (
        (None, {'fields': ["invoice_id", "purchase_date"]}),
        ("Items", {'fields': ["items"]}),
        ("Payment Details", {'fields': ["payment_mode", "payment_status"]}),
        ("Customer Details", {'fields': ["customer"]}),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)



admin.site.register(CustomerDetail, CustomerDetailAdmin)
admin.site.register(SaleRecord, SaleRecordAdmin)
admin.site.register(SaleEffectiveCost)
