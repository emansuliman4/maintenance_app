from django.urls import path
from .views import (
    MachineTypeListView, MachineTypeDetailView,
    MachineListView, MachineDetailView,
    MultiReceptionAndTVListView, MultiReceptionAndTVDetailView,
    AgentListView, AgentDetailView
)

urlpatterns = [
    path('machine-types/', MachineTypeListView.as_view(), name='machine-type-list'),
    path('machine-types/<int:pk>/', MachineTypeDetailView.as_view(), name='machine-type-detail'),
    path('machines/', MachineListView.as_view(), name='machine-list'),
    path('machines/<int:pk>/', MachineDetailView.as_view(), name='machine-detail'),
    path('multi-reception-tv/', MultiReceptionAndTVListView.as_view(), name='multi-reception-tv-list'),
    path('multi-reception-tv/<int:pk>/', MultiReceptionAndTVDetailView.as_view(), name='multi-reception-tv-detail'),
    path('agents/', AgentListView.as_view(), name='agent-list'),
    path('agents/<int:pk>/', AgentDetailView.as_view(), name='agent-detail'),
]
