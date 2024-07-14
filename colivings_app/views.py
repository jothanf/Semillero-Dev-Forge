from rest_framework import viewsets
from .serializer import ColivingSerializer
from .models import ColivingModel

# Create your views here.
class colivingView(viewsets.ModelViewSet):
    serializer_class = ColivingSerializer
    queryset = ColivingModel.objects.all()