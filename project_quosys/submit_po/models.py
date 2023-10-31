from django.db import models
from django.contrib.auth.models import User


class PurchaseOrder(models.Model):
    officer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    company_name = models.CharField(null=True, max_length=100)
    address_line_1 = models.CharField(null=True, max_length=100)
    address_line_2 = models.CharField(null=True, max_length=100)
    city = models.CharField(null=True, max_length=50)
    state = models.CharField(null=True, max_length=20)
    zipcode = models.CharField(null=True, max_length=10)
    contact_name = models.CharField(null=True, max_length=50)
    contact_no  = models.CharField(null=True, max_length=20)

    def __str__(self):
        return self.company_name + " #" + self.poid
    
    @property
    def poid(self):
        return str("PO%04d" % self.id)

class PurchaseOrderItem(models.Model):
    po = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(null=True, max_length=100)
    price = models.DecimalField(default=0.00,max_digits=100, decimal_places=2) 
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    @property
    def total(self):
        return (self.price * self.quantity)