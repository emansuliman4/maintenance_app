from django.urls import path
from .views import (
    CallListView, CallDetailView,
    ReceptionListView, ReceptionDetailView,
    AttachmentListView, InReceptionListView,
    MaintenanceListView, MultiReceptionCustomerListView
)

urlpatterns = [
    path('calls/', CallListView.as_view(), name='call-list'),
    path('calls/<int:pk>/', CallDetailView.as_view(), name='call-detail'),
    path('receptions/', ReceptionListView.as_view(), name='reception-list'),
    path('receptions/<int:pk>/', ReceptionDetailView.as_view(), name='reception-detail'),
    path('attachments/', AttachmentListView.as_view(), name='attachment-list'),
    path('in-receptions/', InReceptionListView.as_view(), name='in-reception-list'),
    path('maintenances/', MaintenanceListView.as_view(), name='maintenance-list'),
    path('multi-reception-customers/', MultiReceptionCustomerListView.as_view(), name='multi-reception-customer-list'),
]
