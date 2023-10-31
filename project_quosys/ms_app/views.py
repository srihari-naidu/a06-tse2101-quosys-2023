from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .models import Purchaseorderreport 
from .models import Sale
from .models import Item, PurchaseRequisition
from django.http import Http404
from datetime import datetime, timedelta
from django.shortcuts import render


from django.contrib.auth.decorators import login_required

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return(redirect('/menu'))
    else:
        return render(
            request,
            'ms_app/index.html',
            {
                'title':'Home Page',
                'year': datetime.now().year,
            }
        )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'ms_app/contact.html',
        {
            'title':'Contact',
            'message':'Dr. Yeoh.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'ms_app/about.html',
        {
            'title': 'Quotation System',
            'message':'Software Engineering Fundamentals TT5L',
            'year':datetime.now().year,
        }
    )

@login_required
def menu(request):
    check_manager = request.user.groups.filter(name='Manager').exists()
    check_salesman = request.user.groups.filter(name='Salesman').exists()

    context = {
            'title':'Main Menu',
            'is_Manager': check_manager,
            'is_Salesman': check_salesman,
            'year':datetime.now().year,
        }
    context['user'] = request.user

    return render(request,'ms_app/menu.html',context)

@login_required
def button1(request):
    """Renders the about page."""
    my_data = Sale.objects.all()
    #my_data = Sale.objects.get (quote_id=quote_id)
    return render(request, 'ms_app/button1.html', {'my_data': my_data})

@login_required
def button2view(request):
    """Renders the about page."""
    my_data = Purchaseorderreport.objects.all()
    return render(request, 'ms_app/button2view.html', {'my_data': my_data})
    
def saved(request):
    assert isinstance(request, HttpRequest)
    return render(request,'ms_app/saved.html')



def report(request):
   if request.method =="POST":
       Fromdate=request.POST.get('Fromdate')
       Todate=request.POST.get('Todate')
       
       searchresult=Purchaseorderreport.objects.filter(PO_date__range=(Fromdate,Todate))
       
       return render (request, 'ms_app/report.html',{'displaydata' :searchresult})
   else: 
       displaydata = Purchaseorderreport.objects.all()
      
       return render(request,'ms_app/report.html',{'displaydata':displaydata})
   
   
   
   
def new(request):
    assert isinstance(request, HttpRequest)
    return render(request,'ms_app/new.html')

def createQuotation(request):
    if request.method == 'POST':
        quote_id = request.POST['quote_id']
        salesstaff_id = request.POST['salesstaff_id']
        cust_id = request.POST['cust_id']
        pr_id = request.POST['pr_id']
        
        qitem =Item.objects.get(item_id=request.POST['qitem'])
        
        quot_date = request.POST['quot_date']
        quo_tprice = request.POST['quo_tprice']
        status = request.POST['status']
        Sale1 = Sale(quote_id=quote_id, salesstaff_id=salesstaff_id, cust_id= cust_id, pr_id=pr_id, qitem=qitem, quot_date=quot_date, quo_tprice=quo_tprice,status=status)
        Sale1.save()
        return redirect('/menu')
    else:
        return render(request, 'ms_app/create_quotation.html')

def viewQuotation(request):
    sales_data = Sale.objects.all()
    return render(request, 'ms_app/view_quotation.html', {'sales_data': sales_data})

def approve(request, quote_id):
    data = Sale.objects.get (quote_id=quote_id)
    item = Sale.objects.all()
    if request.method == 'POST':
        
        quote_id = request.POST['quote_id']
        salesstaff_id = request.POST['salesstaff_id']
        cust_id = request.POST['cust_id']
        pr_id = request.POST['pr_id']
        quot_date = request.POST['quot_date']
        quot_date = datetime.strptime(quot_date, '%b. %d, %Y').strftime('%Y-%m-%d')
        quo_tprice = request.POST['quo_tprice']
        status = request.POST['status']
        
        data.quote_id=quote_id
        data.salesstaff_id=salesstaff_id
        data.cust_id=cust_id
        data.pr_id=pr_id
        data.quot_date=quot_date
        data.quo_tprice=quo_tprice
        data.status=status
        data.save()
        
        
        return redirect ('/menu')
    return render(request, 'ms_app/approve.html', {'data': data, 'item' :item})

def CreatePurchaseRequisition(request):
    if request.method == 'POST':
        purchase_id = request.POST.get('purchase_id')
        customer_id  = request.POST.get('customer_id')
        pitem = Item.objects.get(item_id=request.POST['pitem'])
        pr_date = request.POST.get('pr_date')

        purchase_requisition = PurchaseRequisition(purchase_id=purchase_id, customer_id=customer_id, pitem=pitem, pr_date=pr_date)
        purchase_requisition.save()

        return redirect('/menu')
    else:
        return render(request, 'ms_app/create_purchase_requisition.html')
    
def viewPR(request):
    pr_data = PurchaseRequisition.objects.all()
    return render(request, 'ms_app/view_purchase_requisition.html', {'pr_data': pr_data})