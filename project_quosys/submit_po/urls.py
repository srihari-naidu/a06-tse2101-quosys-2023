from django.urls import path
from .views import POList, PODetail, POCreate, POUpdate, PODelete, delete_poitem

urlpatterns = [
    path('pos', POList.as_view(), name='pos'),
    path('po/<int:pk>', PODetail.as_view(), name='po'),
    path('po-create/', POCreate.as_view(), name='po-create'),
    path('po-update/<int:pk>', POUpdate.as_view(), name='po-update'),
    path('po-delete/<int:pk>', PODelete.as_view(), name='po-delete'),
    path('poitem-delete/<int:pk>', delete_poitem, name='poitem-delete'),
]