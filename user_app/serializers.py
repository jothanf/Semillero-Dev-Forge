from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserAgentModel, UserCustomerModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Crear el usuario utilizando email en lugar de username
        user = User.objects.create_user(
            username=validated_data['email'],  # Asignar el email al campo username
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        return user


class UserAgentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserAgentModel
        fields = ['user', 'phone']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        # Crear el usuario sin 'username', usando 'email' para el campo username
        user = User.objects.create_user(
            username=user_data['email'],  # Asignar el email al campo username
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data.get('last_name', ''),
            password=user_data['password']
        )
        user_agent = UserAgentModel.objects.create(user=user, **validated_data)
        return user_agent
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.phone = validated_data.get('phone', instance.phone)

        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.username = user_data.get('email', user.username)  # Actualizar también el username
        if 'password' in user_data:
            user.set_password(user_data['password'])

        user.save()
        instance.save()

        return instance



class UserCustomerCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserCustomerModel
        fields = ['email', 'password', 'phone', 'buy', 'sell', 'build', 'blog']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("El correo ya se encuentra en uso.")
        return value

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        user_customer = UserCustomerModel.objects.create(
            user=user,
            **validated_data
        )
        return user_customer

class UserCustomerCompleteSerializer(serializers.ModelSerializer):
    agent = serializers.PrimaryKeyRelatedField(queryset=UserAgentModel.objects.all(), allow_null=True, required=False)

    class Meta:
        model = UserCustomerModel
        fields = ['agent', 'phone', 'buy', 'sell', 'build', 'blog']

    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone', instance.phone)
        instance.buy = validated_data.get('buy', instance.buy)
        instance.sell = validated_data.get('sell', instance.sell)
        instance.build = validated_data.get('build', instance.build)
        instance.blog = validated_data.get('blog', instance.blog)
        instance.agent = validated_data.get('agent', instance.agent)

        instance.save()
        return instance


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Correo electrónico no registrado.")

        # Autenticar usando el email como username
        user = authenticate(username=user.email, password=password)

        if user is None:
            raise serializers.ValidationError("Credenciales no válidas.")
        
        if not user.is_active:
            raise serializers.ValidationError("El usuario está inactivo.")

        return {
            'user': user,
        }
