from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .serializers import UserLoginSerializer, UserSerializer, UserAgentSerializer, UserAgentLoginSerializer, UserCustomerSerializer

"""
from rest_framework import viewsets
from django.contrib.auth.models import User

class Userview(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
"""

## Common User
class UserSignupView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario creado con éxito"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSigninView(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "message": "Inicio de sesión exitoso"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSignoutView(APIView):

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({"message": "Cierre de sesión exitoso"}, status=status.HTTP_200_OK)

## Agent User
class UserAgentSignupView(APIView):

    def post(self, request):
        serializer = UserAgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Agente creado con éxito"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserAgentSigninView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserAgentLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            
            # Confirma que el token se ha creado
            if created:
                print(f"Token creado: {token.key}")
            else:
                print(f"Token existente: {token.key}")

            user_agent = serializer.validated_data.get('user_agent')
            return Response({
                "token": token.key,
                "message": "Inicio de sesión exitoso",
                "user_agent": UserAgentSerializer(user_agent).data if user_agent else None
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserAgentSignoutView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        user = request.user
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        logout(request)
        return Response({"message": "Cierre de sesión exitoso"}, status=status.HTTP_200_OK)
    
## Customer User
class UserCustomerSignupView(APIView):

    def post(self, request):
        serializer = UserCustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cliente creado con éxito"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserCustomerSigninView(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "message": "Inicio de sesión exitoso"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserCustomerSignoutView(APIView):
    
    def post(self, request):
        user = request.user
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        logout(request)
        return Response({"message": "Cierre de sesión exitoso"}, status=status.HTTP_200_OK)