from django import forms
from django.forms import inlineformset_factory
from .models import PurchaseOrder, PurchaseOrderItem


class POForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrder
        fields = [
            'company_name', 
            'address_line_1',
            'address_line_2',
            'city',
            'zipcode',
            'state',
            'contact_name',
            'contact_no',
            ]
        widgets = {
            'company_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'address_line_1': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'address_line_2': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'city': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'zipcode': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'state': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'contact_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'contact_no': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
        }

class POItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

POItemFormSet = inlineformset_factory(
    PurchaseOrder, PurchaseOrderItem, form=POItemForm,
    extra=1, can_delete=False
)