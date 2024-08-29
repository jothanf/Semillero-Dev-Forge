from django.urls import path
from .views import PropertyCreateView, PropertyDetailView, PropertyUpdateView, PropertyListView

urlpatterns = [
    path('api/properties/', PropertyListView.as_view(), name='property_list'),
    path('api/properties/create/', PropertyCreateView.as_view(), name='property_create'),
    path('api/properties/<int:pk>/', PropertyDetailView.as_view(), name='property_detail'),
    path('api/properties/<int:pk>/update/', PropertyUpdateView.as_view(), name='property_update'),
]
