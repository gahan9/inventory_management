# coding=utf-8
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.utils.translation import ugettext_lazy as _
from djmoney.models.fields import MoneyField

from core_settings.settings import PRODUCT_TYPE, PRODUCT_MAKER


class PurchaseCompany(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name=_("Company Name"),
                            help_text=_("Enter Name of the company from which you are making your purchase"))
    contact_number = models.IntegerField(blank=True, null=True,
                                         verbose_name=_("Contact Number"))
    alternate_contact_number = models.IntegerField(blank=True, null=True,
                                                   verbose_name=_("Alternate Contact Number"))
    fax_number = models.IntegerField(blank=True, null=True,
                                     verbose_name=_("Fax Number"))
    address = models.TextField(blank=True, null=True)
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


class ProductRecord(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name=_(PRODUCT_TYPE + " Name"),
                            help_text=_("Enter Name/Title of Item"))
    price = MoneyField(decimal_places=2, default=0, default_currency='INR', max_digits=11,
                       verbose_name=_("MRP of " + PRODUCT_TYPE))
    available_stock = models.IntegerField(blank=True, null=True, default=0)
    product_image = models.ImageField(upload_to='media/uploads/', blank=True, null=True)
    launched_by = models.CharField(max_length=300, blank=True, null=True,
                                   verbose_name=_(PRODUCT_MAKER[PRODUCT_TYPE][0] + " Name"))
    product_launch_date = models.DateField(
        blank=True, null=True,
        verbose_name=_("Date of " + PRODUCT_MAKER[PRODUCT_TYPE][1]))
    version = models.IntegerField(
        blank=True, null=True,
        verbose_name="Edition",
        help_text="Enter Version or Edition of Item (if applicable)")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def has_image(self):
        return bool(self.product_image)

    def __str__(self):
        return "{} - {}, ₹{}".format(self.name, self.launched_by, self.price)

    class Meta:
        verbose_name = verbose_name_plural = PRODUCT_TYPE + " Detail"


class EffectiveCost(models.Model):
    discount = models.IntegerField(default=10)
    cost = models.ForeignKey(ProductRecord, on_delete=models.CASCADE)
    effective_cost = MoneyField(decimal_places=2, default=0,
                                default_currency='INR', max_digits=11,
                                verbose_name=_("Effective cost"))
    total_effective_cost = MoneyField(decimal_places=2, default=0,
                                      default_currency='INR', max_digits=11,
                                      verbose_name=_("Total Effective cost"),
                                      blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)

    @property
    def details(self):
        return model_to_dict(self)

    def get_detail(self):
        return "{} -₹{} @{}%= ₹{}; ₹{} per item ₹{} for total item".format(
            self.cost.name, self.cost.price, self.discount,
            self.effective_cost, self.quantity, self.total_effective_cost)

    def clean(self):
        self.effective_cost = (self.cost.price.amount * (100 - self.discount)) / 100
        self.total_effective_cost = self.quantity * self.effective_cost
        self.cost.available_stock = self.cost.available_stock + self.quantity

    def __str__(self):
        return "{} - {}% @ {}".format(self.cost.name, self.discount, self.cost.price)

    class Meta:
        verbose_name = verbose_name_plural = "Effective cost of " + PRODUCT_TYPE


class PurchaseRecord(models.Model):
    PAYMENT_MODE = (
        (1, _("Cash")),
        (2, _("Cheque")),
        (3, _("Online Transfer NEFT/RTGS")),
        (4, _("Demand Draft")),
    )
    invoice_id = models.CharField(max_length=80, blank=True, null=True,
                                  verbose_name=_("Enter Invoice Number"),
                                  help_text=_("Enter Order/Invoice Number"))
    purchased_from = models.ForeignKey(
        PurchaseCompany, on_delete=models.CASCADE,
        verbose_name=_("Supplier Name"),
        help_text=_("Choose Company from where purchase is made"))
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
    items = models.ManyToManyField(EffectiveCost, blank=True)
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

    @property
    def get_items(self):
        return [p.get_detail for p in self.items.all()]

    def __str__(self):
        return self.invoice_id

    class Meta:
        verbose_name = "Purchase Details of " + PRODUCT_TYPE
        verbose_name_plural = "Purchase Details of item from various suppliers"


@receiver(pre_save, sender=PurchaseRecord, dispatch_uid="calculate_total_amount")
def calculate_total_amount(sender, instance, created, *args, **kwargs):
    # print("post_save : signal", sender, instance, created, kwargs, args)
    total_amount = sum([product['total_effective_cost'] for product in instance.items.values()])
    if instance.total_amount.amount != total_amount:
        instance.total_amount = sum([product['total_effective_cost'] for product in instance.items.values()])
        # instance.save()
