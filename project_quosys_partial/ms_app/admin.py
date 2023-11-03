from django.contrib import admin
from ms_app.models import Item
from ms_app.models import Purchaseorderreport, PurchaseRequisition
from . models import Sale

admin.site.register(Item)
admin.site.register(Purchaseorderreport)

class SalesAdmin(admin.ModelAdmin):
    list_display = ('quote_id', 'salesstaff_id', 'cust_id' , 'pr_id' ,'qitem','quot_date','quo_tprice','status')
admin.site.register(Sale,SalesAdmin)

class PRAdmin(admin.ModelAdmin):
    display2 = ('purchase_id','customer_id ','pitem','pr_date')
admin.site.register(PurchaseRequisition,PRAdmin)