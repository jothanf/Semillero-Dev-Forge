from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from .serializers import (
    UserAgentSerializer, 
    SignInSerializer, 
    UserCustomerCreateSerializer, 
    UserCustomerCompleteSerializer
)
from .models import UserCustomerModel

# Crear UserAgent
class UserAgentSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserAgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Agente creado con éxito"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Cerrar sesión UserAgent
class UserAgentSignoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()  # Eliminar el token
        logout(request)
        
        # Eliminar la cookie HttpOnly
        response = Response({"message": "Cierre de sesión exitoso"}, status=status.HTTP_200_OK)
        response.delete_cookie('auth_token')  # Eliminar cookie
        
        return response

# Crear UserCustomer (registro inicial)
class UserCustomerInitialSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCustomerCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Usuario creado con éxito", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Completar perfil de UserCustomer
class UserCustomerCompleteSignupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_customer = UserCustomerModel.objects.get(user=request.user)
        except UserCustomerModel.DoesNotExist:
            return Response({"error": "Usuario cliente no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserCustomerCompleteSerializer(user_customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Información de cliente completada con éxito"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Cerrar sesión UserCustomer
class UserCustomerSignoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()  # Eliminar el token
        logout(request)
        
        # Eliminar la cookie HttpOnly
        response = Response({"message": "Cierre de sesión exitoso"}, status=status.HTTP_200_OK)
        response.delete_cookie('auth_token')  # Eliminar cookie
        
        return response

# Iniciar sesión UserAgent y UserCustomer
class UserSigninView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            # Determinar el tipo de usuario
            user_agent = None
            if hasattr(user, 'useragentmodel'):
                user_type = 'agent'
                user_agent = user.useragentmodel
                user_data = UserAgentSerializer(user_agent).data
            elif hasattr(user, 'usercustomermodel'):
                user_type = 'customer'
                user_agent = user.usercustomermodel
                user_data = UserCustomerCompleteSerializer(user_agent).data
            else:
                user_type = 'unknown'
                user_data = None

            # Crear respuesta con token como cookie HttpOnly
            response = Response({
                "token": token.key,
                "message": "Inicio de sesión exitoso",
                "user_type": user_type,
                "user_data": user_data
            }, status=status.HTTP_200_OK)
            
            # Configurar la cookie HttpOnly
            response.set_cookie(
                key='auth_token',
                value=token.key,
                httponly=True,
                samesite='Lax',
                secure=True 
            )
            
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
