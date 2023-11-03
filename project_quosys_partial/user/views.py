from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import Group

from user.functions import *

class AppLoginView(LoginView):
    template_name = 'user/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        if is_manager(self.request.user):
            return reverse_lazy('menu')
        elif is_finance_officer(self.request.user):
            return reverse_lazy('pos')
        elif is_salesman(self.request.user):
            return reverse_lazy('menu')
        elif is_customer(self.request.user):
            return reverse_lazy('menu')

class RegisterView(FormView):
    template_name = 'user/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name='Customer')
        group.user_set.add(user)
        return super(RegisterView, self).form_valid(form)