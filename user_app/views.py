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
    
## Verificación con Oauth2
from django.shortcuts import redirect
from google_auth_oauthlib.flow import Flow
import os

import os
from django.shortcuts import redirect
from google_auth_oauthlib.flow import Flow
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Permitir OAuth inseguro en desarrollo

def oauth2_callback(request):
    flow = Flow.from_client_secrets_file(
        os.path.join(os.path.dirname(__file__), 'credentials.json'),
        scopes=['https://www.googleapis.com/auth/gmail.send'],
        redirect_uri='http://localhost:8000/oauth2callback/'
    )
    
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials

    # Aquí puedes almacenar las credenciales o usarlas para hacer peticiones a Gmail
    # Por ejemplo, puedes guardarlas en la sesión del usuario
    request.session['credentials'] = credentials_to_dict(credentials)

    return redirect('/')  # Redirige a la página principal o a donde prefieras

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

def start_auth_flow(request):
    flow = Flow.from_client_secrets_file(
        os.path.join(os.path.dirname(__file__), 'credentials.json'),
        scopes=['https://www.googleapis.com/auth/gmail.send'],
        redirect_uri='http://localhost:8000/oauth2callback/'
    )
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return redirect(authorization_url)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserCustomerCreateSerializer
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os

class UserCustomerOAuth2SignupView(APIView):
    @swagger_auto_schema(
        request_body=UserCustomerCreateSerializer,
        responses={
            200: openapi.Response(description="Correo de verificación enviado"),
            400: openapi.Response(description="Error en los datos enviados"),
            401: openapi.Response(description="Error de autenticación con Google")
        }
    )
    def post(self, request):
        serializer = UserCustomerCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Guardar los datos del usuario temporalmente
            user_data = serializer.validated_data
            
            # Obtener credenciales de OAuth2
            creds = self.get_oauth2_credentials()
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    return Response({"error": "Se requiere autenticación con Google"}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Enviar correo de verificación
            success = self.send_verification_email(creds, user_data['email'])
            
            if success:
                # Almacenar los datos del usuario en sesión o cache para completar el registro después
                request.session['pending_user_data'] = user_data
                return Response({"message": "Correo de verificación enviado"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Error al enviar el correo de verificación"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_oauth2_credentials(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        return creds

    def send_verification_email(self, creds, email):
        try:
            service = build('gmail', 'v1', credentials=creds)
            message = self.create_verification_message(email)
            service.users().messages().send(userId="me", body=message).execute()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def create_verification_message(self, to):
        # Implementa la lógica para crear el mensaje de verificación
        # Puedes incluir un token de verificación en el enlace
        pass


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.models import User
from .models import UserCustomerModel
from django.core.exceptions import ObjectDoesNotExist

class VerifyEmailView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('token', openapi.IN_QUERY, description="Token de verificación", type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response(description="Correo verificado exitosamente"),
            400: openapi.Response(description="Token inválido o expirado")
        }
    )
    def get(self, request):
        token = request.GET.get('token')
        
        if not token:
            return Response({"error": "Token no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Aquí deberías implementar la lógica para verificar el token
        # Por ejemplo, podrías tener una tabla en la base de datos que almacene los tokens y sus fechas de expiración
        
        try:
            # Supongamos que tienes una función que verifica el token y devuelve los datos del usuario
            user_data = self.verify_token(token)
            
            # Crear el usuario y el perfil de cliente
            user = User.objects.create_user(
                username=user_data['email'],
                email=user_data['email'],
                password=user_data['password']
            )
            
            UserCustomerModel.objects.create(
                user=user,
                phone=user_data.get('phone'),
                buy=user_data.get('buy', False),
                sell=user_data.get('sell', False),
                build=user_data.get('build', False),
                blog=user_data.get('blog', False)
            )
            
            return Response({"message": "Correo verificado y cuenta creada exitosamente"}, status=status.HTTP_200_OK)
        
        except ObjectDoesNotExist:
            return Response({"error": "Token inválido o expirado"}, status=status.HTTP_400_BAD_REQUEST)

    def verify_token(self, token):
        # Implementa la lógica para verificar el token
        # Esto podría implicar consultar una base de datos o un servicio de caché
        pass