from rest_framework import serializers
from .models import PropertyModel

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyModel
        fields = ['id', 'owner', 'address', 'price', 'area']

    def create(self, validated_data):
        return PropertyModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address)
        instance.price = validated_data.get('price', instance.price)
        instance.area = validated_data.get('area', instance.area)
        instance.save()
        return instance
