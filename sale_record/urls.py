from django.urls import path

from .views import *

urlpatterns = [
    path('generate_invoice/<int:pk>/', InvoiceGenerateView.as_view(), name="generate_invoice"),
    path('se_lab/', TableTemplateView.as_view(), name="table_display"),
]
