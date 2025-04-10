from django.urls import path
from .views import CustomerListView, CustomerDetailView, CustomerPhoneListView, CustomerPhoneDetailView

urlpatterns = [
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('customer-phones/', CustomerPhoneListView.as_view(), name='customer-phone-list'),
    path('customer-phones/<int:pk>/', CustomerPhoneDetailView.as_view(), name='customer-phone-detail'),
]
