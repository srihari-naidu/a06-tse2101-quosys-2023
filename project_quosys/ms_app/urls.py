from django.urls import path, re_path
from . import views


urlpatterns = [
    path('approve/<int:quote_id>', views.approve, name='approve'),
    path('update/<int:quote_id>', views.saved, name='saved'),
    
    re_path(r'^$', views.home, name='home'),
    re_path(r'^contact$', views.contact, name='contact'),
    re_path(r'^about$', views.about, name='about'),
    re_path(r'^menu$', views.menu, name='menu'),
    
    re_path(r'^button1$', views.button1, name='button1'),
    re_path(r'^button2view$', views.button2view, name='button2view'),
    re_path(r'saved', views.saved, name='saved'),
    re_path(r'report', views.report, name='report'),
    re_path(r'CreateQuotation',views.createQuotation,name='Create Quotation'),
    re_path(r'ViewQuotation',views.viewQuotation,name='View Quotation'),
    re_path(r'CreatePurchaseRequisition',views.CreatePurchaseRequisition,name='Create Purchase Requisition'),
    re_path(r'ViewPurchaseRequisition',views.viewPR,name='View Purchase Requisition'),
]