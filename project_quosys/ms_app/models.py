"""
Definition of models.
"""

from django.db import models

from django.contrib.auth.models import User

#sharing entity

class Item(models.Model):
    item_id = models.CharField(primary_key=True, max_length=10)
    item_name = models.TextField()
    item_description = models.TextField(null=True,default=None, blank=True)
    def __str__(self):
        return str(self.item_id)

class Purchaseorderreport(models.Model):
    PO_id =models.IntegerField(primary_key = True, default ="")
    finance_id =models.IntegerField(default ="")
    PO_date =models.DateField()
    PO_tprice =models.IntegerField(default ="")
    def __str__(self):
        return str(self.PO_id)

class Sale(models.Model):
    quote_id = models.IntegerField(primary_key=True)
    salesstaff_id = models.IntegerField()
    cust_id = models.IntegerField()
    pr_id = models.IntegerField()
    qitem = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    quot_date = models.DateField()
    quo_tprice = models.IntegerField()
    status = models.CharField(max_length=255,default='pending')

class PurchaseRequisition(models.Model):
    purchase_id = models.IntegerField(primary_key=True)
    customer_id = models.IntegerField()
    pitem = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    pr_date = models.DateField()
    
