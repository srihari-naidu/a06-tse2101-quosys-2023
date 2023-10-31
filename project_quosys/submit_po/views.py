from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F, Sum
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from user.functions import is_finance_officer

from .forms import POForm, POItemFormSet
from .models import PurchaseOrder, PurchaseOrderItem


class POList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = PurchaseOrder
    context_object_name = 'pos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pos'] = context['pos'].filter(officer=self.request.user)
        context['count'] = context['pos'].count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['pos'] = context['pos'].filter(
                company_name__startswith = search_input
                )
        context['search'] = search_input
        return context

    def test_func(self):
        return is_finance_officer(self.request.user)

class PODetail(LoginRequiredMixin, DetailView):
    model = PurchaseOrder
    context_object_name = 'po'
    template_name = 'submit_po/purchaseorder.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['poitems'] = PurchaseOrderItem.objects.filter(po=context['po'].id)
        
        context['total'] = context['poitems'].annotate(total=Sum(F('price') * F('quantity')))
        context['total'] = '{:0.2f}'.format(
            (context['total'].aggregate(Sum('total',default=Decimal(0.00)))['total__sum'])
            )

        return context

class PODelete(LoginRequiredMixin, DeleteView):
    model = PurchaseOrder
    context_object_name = 'po'
    success_url = reverse_lazy('pos')


 
class POInline():
    form_class = POForm
    model = PurchaseOrder
    template_name = "submit_po/purchaseorder_create_or_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('pos')

    def formset_poitems_valid(self, formset):
        """
        Hook for custom formset saving. Useful if you have multiple formsets
        """
        poitems = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for poitem in poitems:
            poitem.po = self.object
            poitem.save()


class POCreate(LoginRequiredMixin, POInline, CreateView):
    model = PurchaseOrder
    success_url = reverse_lazy('pos')
    
    def form_valid(self, form):
        form.instance.officer = self.request.user
        return super(POCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(POCreate, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        return context

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'poitems': POItemFormSet(prefix='poitems'),
            }
        else:
            return {
                'poitems': POItemFormSet(self.request.POST or None, self.request.FILES or None, prefix='poitems'),
            }


class POUpdate(LoginRequiredMixin, POInline, UpdateView):
    model = PurchaseOrder
    success_url = reverse_lazy('pos')

    def get_context_data(self, **kwargs):
        context = super(POUpdate, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        return context

    def get_named_formsets(self):
        return {
            'poitems': POItemFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='poitems'),
        }

'''
This 2 functions are for custom added delete button functionality. 
If you don't want to use custom delete buttons than don't add this.
'''

def delete_poitem(request, pk):
    try:
        poitem = PurchaseOrderItem.objects.get(id=pk)
    except PurchaseOrderItem.DoesNotExist:
        messages.success(
            request, 'Item does not exit'
            )
        return redirect('po-update', pk=poitem.po.id)

    poitem.delete()
    messages.success(
            request, 'Item deleted successfully'
            )
        
    return redirect('po-update', pk=poitem.po.id)