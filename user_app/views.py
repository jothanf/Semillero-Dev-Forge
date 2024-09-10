from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from .models import UserCustomerModel
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    UserAgentSerializer, 
    SignInSerializer, 
    UserCustomerCreateSerializer, 
    UserCustomerCompleteSerializer
)


# Crear UserAgent    
class UserAgentSignupView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UserAgentSerializer,
        responses={
            201: openapi.Response(description="Agente creado con éxito"),
            400: openapi.Response(description="Error en los datos enviados")
        }
    )
    def post(self, request):
        serializer = UserAgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Agente creado con éxito"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Cerrar sesión UserAgent
class UserAgentSignoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description="Cierre de sesión exitoso"),
            401: openapi.Response(description="No autorizado")
        }
    )
    def post(self, request):
        user = request.user
        if hasattr(user, 'auth_token'):
            user.auth_token.delete() 
        logout(request)
        
        response = Response({"message": "Cierre de sesión exitoso"}, status=status.HTTP_200_OK)
        response.delete_cookie('auth_token')
        
        return response

# Crear UserCustomer (registro inicial)
class UserCustomerInitialSignupView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UserCustomerCreateSerializer,
        responses={
            201: openapi.Response(description="Usuario creado con éxito"),
            400: openapi.Response(description="Error en los datos enviados")
        }
    )

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

    @swagger_auto_schema(
        request_body=UserCustomerCompleteSerializer,
        responses={
            200: openapi.Response(description="Información de cliente completada con éxito"),
            400: openapi.Response(description="Error en los datos enviados"),
            404: openapi.Response(description="Usuario cliente no encontrado")
        }
    )

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

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description="Cierre de sesión exitoso"),
            401: openapi.Response(description="No autorizado")
        }
    )

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

    @swagger_auto_schema(
        request_body=SignInSerializer,
        responses={
            200: openapi.Response(
                description="Inicio de sesión exitoso",
                examples={
                    'application/json': {
                        "message": "Inicio de sesión exitoso",
                        "user_type": "UserAgent or UserCustomer"
                    }
                }
            ),
            400: openapi.Response(description="Error en los datos enviados")
        }
    )

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

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description="Sesión activa"),
            401: openapi.Response(description="No autorizado")
        }
    )

    def get(self, request, format=None):
        return Response({'is_authenticated': True, 'user_name': request.user.username})
    
"""

def ConsultarUsuarioCustomerPorId(username or== mail):
    return user.buy, user.sell, user.build, user.blog, user.phone

"""
class ConsultUserCustomerById(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Consulta los datos de un usuario cliente por ID",
        manual_parameters=[
            openapi.Parameter(
                'id', 
                openapi.IN_PATH, 
                description="ID del usuario cliente", 
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: openapi.Response(
                description="Datos del usuario cliente",
                schema=UserCustomerCompleteSerializer()
            ),
            404: "Usuario cliente no encontrado",
            400: "El usuario no ha completado el segundo registro"
        }
    )
    def get(self, request, id):
        user_customer = get_object_or_404(UserCustomerModel, user__id=id)

        # Verificar si el usuario ha completado el segundo registro
        if not (user_customer.phone or user_customer.buy or user_customer.sell or user_customer.build or user_customer.blog):
            return Response(
                {"error": "El usuario no ha completado el segundo registro"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserCustomerCompleteSerializer(user_customer)
        return Response(serializer.data)