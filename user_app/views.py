from rest_framework_simplejwt.tokens import RefreshToken
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
from django.contrib.auth.models import User

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
        
        response = Response({"message": "Cierre de sesión exitoso"}, status=status.HTTP_200_OK)
        response.delete_cookie('auth_token')  # Eliminar cookie
        
        return response

# Crear UserCustomer (registro inicial)
class UserCustomerInitialSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCustomerCreateSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            
            user_customer = UserCustomerModel.objects.create(user=user)
            
            return Response({
                "message": "Usuario creado con éxito", 
                "user_id": user_customer.user.id
            }, status=status.HTTP_201_CREATED)
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

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response({
                "message": "Inicio de sesión exitoso"
            }, status=status.HTTP_200_OK)
           
            response.set_cookie(
                key='access',
                value=access_token,
                httponly=True,
                secure=True,  
                samesite='Lax'  
            )

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Iniciar sesión UserAgent y UserCustomer
class UserSigninView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Determinar el tipo de usuario
            if hasattr(user, 'useragentmodel'):
                user_type = 'UserAgent'
            elif hasattr(user, 'usercustomermodel'):
                user_type = 'UserCustomer'
            else:
                user_type = 'Unknown'

            response = Response({
                "message": "Inicio de sesión exitoso",
                "user_type": user_type
            }, status=status.HTTP_200_OK)

            response.set_cookie(
                key='access',
                value=access_token,
                httponly=True,
                secure=True,  
                samesite='Lax'  
            )

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Verificar sesión
class CheckSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response({'is_authenticated': True, 'user_name': request.user.username})
