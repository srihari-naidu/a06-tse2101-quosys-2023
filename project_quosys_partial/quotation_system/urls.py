from django.urls import path
from .views import HomeView
from user.views import AppLoginView

urlpatterns = [
    # path('', AppLoginView.as_view(), name='login'),
    # path('', HomeView.as_view(), name='home'),
]