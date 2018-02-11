# coding=utf-8
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from djmoney.models.fields import MoneyField

from core_settings.settings import PRODUCT_TYPE, PRODUCT_MAKER


class PurchaseCompany(models.Model):
    name = models.CharField(max_length=200, verbose_name="Company Name",
                            help_text="Enter Name of the company from which you are making your purchase")
    contact_number = models.IntegerField(blank=True, null=True, verbose_name="Contact Number")
    alternate_contact_number = models.IntegerField(blank=True, null=True, verbose_name="Alternate Contact Number")
    fax_number = models.IntegerField(blank=True, null=True, verbose_name="Fax Number")
    address = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Supplier detail"
        verbose_name_plural = "Supplier Details"


class ProductRecord(models.Model):
    name = models.CharField(max_length=200, verbose_name=PRODUCT_TYPE + " Name",
                            help_text="Enter Name/Title of Item")
    price = MoneyField(decimal_places=2, default=0, default_currency='INR', max_digits=11,
                       verbose_name="MRP of " + PRODUCT_TYPE)
    available_stock = models.IntegerField(blank=True, null=True, default=0)
    product_image = models.ImageField(upload_to='media/uploads/', blank=True, null=True)
    product_launch_date = models.DateField(blank=True, null=True, verbose_name="Date of Publish")
    launched_by = models.CharField(max_length=300, blank=True, null=True, verbose_name=PRODUCT_MAKER[PRODUCT_TYPE] + " Name")
    version = models.IntegerField(blank=True, null=True, verbose_name="Edition",
                                  help_text="Enter Version or Edition of Item")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}, ₹{}".format(self.name, self.launched_by, self.price)

    class Meta:
        verbose_name = verbose_name_plural = PRODUCT_TYPE + " Detail"


class EffectiveCost(models.Model):
    discount = models.IntegerField(default=10)
    cost = models.ForeignKey(ProductRecord, on_delete=models.CASCADE)
    effective_cost = MoneyField(decimal_places=2, default=0, default_currency='INR', max_digits=11,
                                verbose_name="Effective cost")
    total_effective_cost = MoneyField(decimal_places=2, default=0, default_currency='INR', max_digits=11,
                                      verbose_name="Total Effective cost", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)

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
        (1, "Cash"),
        (2, "Cheque"),
        (3, "Online Transfer NEFT/RTGS"),
        (4, "Demand Draft"),
    )
    invoice_id = models.CharField(max_length=80, blank=True, null=True,
                                  verbose_name="Enter Invoice Number",
                                  help_text="Enter Order/Invoice Number")
    purchased_from = models.ForeignKey(PurchaseCompany, on_delete=models.CASCADE,
                                       verbose_name="Purchased From",
                                       help_text="Choose Company from where purchase is made")
    purchase_date = models.DateField(blank=True, null=True, help_text="Enter date of purchase/invoice")
    delivery_date = models.DateField(blank=True, null=True, help_text="Date of order received")
    total_amount = MoneyField(decimal_places=2, default=0, default_currency='INR', max_digits=11,
                              verbose_name="Total Invoice Amount", blank=True, null=True,
                              help_text="Total Payable Invoice Amount [Discounted Rate]")
    items = models.ManyToManyField(EffectiveCost, blank=True)
    payment_mode = models.IntegerField(choices=PAYMENT_MODE, blank=True, null=True)
    paid = models.BooleanField(default=False, verbose_name="Payment Status",
                               help_text="Update payment status if order is paid")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.payment_mode:
            self.paid = True
        else:
            self.paid = False
        val = sum([product['total_effective_cost'] for product in self.items.values()])
        return val

    def __str__(self):
        return self.invoice_id

    class Meta:
        verbose_name = "Purchase Details of " + PRODUCT_TYPE
        verbose_name_plural = "Purchase Details of item from various suppliers"


@receiver(post_save, sender=PurchaseRecord, dispatch_uid="calculate_total_amount")
def calculate_total_amount(sender, instance, created, *args, **kwargs):
    # print("post_save : signal", sender, instance, created, kwargs, args)
    total_amount = sum([product['total_effective_cost'] for product in instance.items.values()])
    if instance.total_amount.amount != total_amount:
        instance.total_amount = sum([product['total_effective_cost'] for product in instance.items.values()])
        instance.save()
