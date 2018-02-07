# coding=utf-8
from django.db import models
from djmoney.models.fields import MoneyField


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
        verbose_name_plural = "Purchase Companies"


class ProductRecord(models.Model):
    name = models.CharField(max_length=200, verbose_name="Product Name",
                            help_text="Enter Name/Title of Item")
    price = MoneyField(decimal_places=2, default=0, default_currency='INR', max_digits=11,
                       verbose_name="MRP of Product")
    product_image = models.ImageField(upload_to='media/uploads/', blank=True, null=True)
    product_launch_date = models.DateField(blank=True, null=True, verbose_name="Date of Publish")
    launched_by = models.CharField(max_length=300, blank=True, null=True, verbose_name="Publisher Name")
    version = models.IntegerField(blank=True, null=True, verbose_name="Edition",
                                  help_text="Enter Version or Edition of Item")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class EffectiveCost(models.Model):
    discount = models.IntegerField(default=10)
    cost = models.ForeignKey(ProductRecord, on_delete=models.CASCADE)
    effective_cost = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}% @ {}".format(self.cost.name, self.discount, self.cost.price)

    class Meta:
        verbose_name = verbose_name_plural = "Effective Cost"


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
    total_amount = models.IntegerField(blank=True, null=True)
    items = models.ManyToManyField(EffectiveCost, blank=True)
    payment_mode = models.IntegerField(choices=PAYMENT_MODE, blank=True, null=True)
    paid = models.BooleanField(default=False, verbose_name="Payment Status",
                               help_text="Update payment status if order is paid")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
