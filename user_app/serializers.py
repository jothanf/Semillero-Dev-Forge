from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserAgentModel, UserCustomerModel

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            raise serializers.ValidationError("Credenciales no válidas.")
        
        if not user.is_active:
            raise serializers.ValidationError("Usuario inactivo.")
        
        return {
            'user': user
        }


class UserAgentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserAgentModel
        fields = ['user', 'nickname', 'phone']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        user_agent = UserAgentModel.objects.create(user=user, **validated_data)
        return user_agent
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.telefono = validated_data.get('telefono', instance.telefono)

        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        if 'password' in user_data:
            user.set_password(user_data['password'])

        user.save()
        instance.save()

        return instance
    
class UserAgentLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        
        if user is None:
            raise serializers.ValidationError("Credenciales no válidas.")
        
        if not user.is_active:
            raise serializers.ValidationError("Usuario inactivo.")
        
        try:
            user_agent = UserAgentModel.objects.get(user=user)
        except UserAgentModel.DoesNotExist:
            raise serializers.ValidationError("El usuario no es un agente.")
        
        return {
            'user': user,
            'user_agent': user_agent
        }
    
class UserCustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    agent = serializers.PrimaryKeyRelatedField(queryset=UserAgentModel.objects.all())

    class Meta:
        model = UserCustomerModel
        fields = ['user', 'agent', 'phone', 'owner']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        return UserCustomerModel.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.phone = validated_data.get('phone', instance.phone)
        instance.owner = validated_data.get('owner', instance.owner)

        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        if 'password' in user_data:
            user.set_password(user_data['password'])

        user.save()
        instance.save()

        return instance
