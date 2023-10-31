from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'quotation_system/home.html'
    success_url = reverse_lazy('login')