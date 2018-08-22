import os
import json
import requests
from django.http import HttpResponse, HttpResponseBadRequest, FileResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from django.views.generic.base import View
from reportlab.pdfgen import canvas
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from core_settings.settings import INV_ROOT
from main.serializers import TempAPISerializer
from main.utils import draw_pdf
from sale_record.models import *
from sale_record.models import TempAPI

__author__ = "Gahan Saraiya"


class InvoiceGenerateView(View):
    def get(self, request, **kwargs):
        print("Generating invoice..")
        pk = self.kwargs.get("pk")
        try:
            sale_invoice = SaleRecord.objects.get(pk=pk)
            print("Found invoice id: {}".format(sale_invoice.invoice_id))
            file_name = "{}_{}.pdf".format(sale_invoice.invoice_id, sale_invoice.printable_sale_date)
            file_location = os.path.join(INV_ROOT, file_name)
            draw_pdf(file_location, sale_invoice)
            return FileResponse(open(file_location, "rb"), content_type="application/pdf")
        except SaleRecord.DoesNotExist as e:
            err_msg = str(e)
            response = "No invoice exist for given query"
            return HttpResponse(response)


class TableTemplateView(TemplateView):
    template_name = "table_display.html"

    def get_json(self):
        json_url = "https://raw.githubusercontent.com/gahan9/SE_lab/master/practical_1/data.json"
        response = requests.get(json_url)
        return response.json()

    def get_context_data(self, **kwargs):
        query_params = self.request.GET
        context = super().get_context_data()
        context["process_model"] = self.get_json().get("process_models", [])
        context["skip_reference"] = int(query_params.get("skip_reference", 1))
        context["skip_image"] = int(query_params.get("skip_image", 0))
        return context


class TempAPIViewSet(viewsets.ModelViewSet):
    serializer_class = TempAPISerializer
    queryset = TempAPI.objects.all().order_by("-date_created")
    permission_classes = [AllowAny]
