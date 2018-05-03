# coding=utf-8
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from djmoney.models.fields import MoneyField

from core_settings.settings import PRODUCT_TYPE

__author__ = "Gahan Saraiya"

__all__ = ['BaseDistributor', 'BaseEffectiveCost', 'BaseProductRecord', 'BasePurchaseRecord']


class BaseDistributor(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name=_("Company Name"),
                            help_text=_("Enter Name of the company from which you are making your purchase"))
    contact_number = models.IntegerField(blank=True, null=True,
                                         verbose_name=_("Contact Number"))
    alternate_contact_number = models.IntegerField(blank=True, null=True,
                                                   verbose_name=_("Alternate Contact Number"))
    fax_number = models.IntegerField(blank=True, null=True,
                                     verbose_name=_("Fax Number"))
    address = models.TextField(_("Postal Address"), blank=True, null=True,
                               help_text=_("Address of distributor"))
    email_address = models.EmailField(blank=True, null=True,
                                      verbose_name=_("Email Address"),
                                      help_text=_("i.e. example@domain.com"))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def has_fax_number(self):
        return bool(self.fax_number)

    @property
    def has_email(self):
        return bool(self.email_address)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Supplier detail"
        verbose_name_plural = "Supplier Details"


class BaseProductRecord(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name=_(PRODUCT_TYPE + " Name"),
                            help_text=_("Enter Name/Title of Item"))
    price = MoneyField(decimal_places=2, default=0, default_currency='INR', max_digits=11,
                       verbose_name=_("MRP of " + PRODUCT_TYPE))
    available_stock = models.IntegerField(blank=True, null=True, default=0)
    product_image = models.ImageField(upload_to='media/uploads/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def has_image(self):
        return bool(self.product_image)

    @property
    def get_image(self):
        if self.has_image:
            return self.product_image.url
        else:
            return None

    def __str__(self):
        return "{} @ {}".format(self.name, self.price)

    class Meta:
        abstract = True
        verbose_name = verbose_name_plural = PRODUCT_TYPE + " Detail"


class BaseEffectiveCost(models.Model):
    discount = models.IntegerField(default=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)

    @property
    def details(self):
        return self.__dict__

    class Meta:
        abstract = True
        verbose_name = verbose_name_plural = "Effective cost of " + PRODUCT_TYPE


class BasePurchaseRecord(models.Model):
    PAYMENT_MODE = (
        (1, _("Cash")),
        (2, _("Cheque")),
        (3, _("Online Transfer NEFT/RTGS")),
        (4, _("Demand Draft")),
    )
    invoice_id = models.CharField(max_length=80, blank=True, null=True,
                                  verbose_name=_("Enter Invoice Number"),
                                  help_text=_("Enter Order/Invoice Number"))

    purchase_date = models.DateField(blank=True, null=True,
                                     help_text=_("Enter date of purchase/invoice"))
    delivery_date = models.DateField(blank=True, null=True,
                                     help_text=_("Date of order received"))
    total_amount = MoneyField(
        decimal_places=2, default=0,
        blank=True, null=True,
        default_currency='INR', max_digits=11,
        verbose_name=_("Total Invoice Amount"),
        help_text=_("Total Payable Invoice Amount [Discounted Rate]"))
    payment_mode = models.IntegerField(choices=PAYMENT_MODE, blank=True, null=True)
    payment_status = models.BooleanField(
        default=False,
        verbose_name=_("Payment Status (in transit/dispute)"),
        help_text=_("mark if payment isn't processed immediately"))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def is_paid(self):
        # to test a case - if payment mode is specified then paid status needs to be true
        return bool(self.payment_mode)

    def __str__(self):
        return self.invoice_id

    class Meta:
        verbose_name = "Purchase Details of " + PRODUCT_TYPE
        verbose_name_plural = "Purchase Details of item from various suppliers"

