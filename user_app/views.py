from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from .serializers import UserAgentSerializer, SignInSerializer, UserCustomerSerializer

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

# Crear UserCustomer
class UserCustomerSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cliente creado con éxito"}, status=status.HTTP_201_CREATED)
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
            elif hasattr(user, 'usercustomermodel'):
                user_type = 'customer'
                user_agent = user.usercustomermodel
            else:
                user_type = 'unknown'
                user_agent = None

            # Crear respuesta con token como cookie HttpOnly
            response = Response({
                "token": token.key,
                "message": "Inicio de sesión exitoso",
                "user_type": user_type,
                "user_data": UserAgentSerializer(user_agent).data if user_type == 'agent' else UserCustomerSerializer(user_agent).data if user_type == 'customer' else None
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
