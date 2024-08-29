from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import PropertyModel
from .serializers import PropertySerializer

class PropertyCreateView(generics.CreateAPIView):
    queryset = PropertyModel.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]

class PropertyDetailView(generics.RetrieveAPIView):
    queryset = PropertyModel.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]

class PropertyUpdateView(generics.UpdateAPIView):
    queryset = PropertyModel.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]

class PropertyListView(generics.ListAPIView):
    queryset = PropertyModel.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]
