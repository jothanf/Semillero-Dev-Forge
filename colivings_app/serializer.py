from rest_framework import serializers
from .models import ColivingModel

class ColivingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColivingModel
        fields = '__all__'