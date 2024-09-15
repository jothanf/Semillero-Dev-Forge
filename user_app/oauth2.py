from django.shortcuts import redirect
from google_auth_oauthlib.flow import InstalledAppFlow
from django.http import HttpResponseBadRequest
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import os
import pickle

def oauth2_callback(request):
    state = request.GET.get('state', None)
    flow = Flow.from_client_secrets_file(
        os.path.join(os.getcwd(), 'credentials.json'),
        scopes=['https://www.googleapis.com/auth/gmail.send'],
        state=state
    )
    flow.redirect_uri = request.build_absolute_uri('/oauth2callback/')

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    
    # Almacenar las credenciales para el usuario
    # Este es un ejemplo simple. En la práctica, querrá asociar esto con la sesión o cuenta del usuario
    with open('token.pickle', 'wb') as token:
        pickle.dump(credentials, token)

    return redirect('/')  # Redireccionar a su página deseada después de la autenticación exitosa

from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import pickle

def get_oauth2_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(os.getcwd(), 'credentials.json'),
                ['https://www.googleapis.com/auth/gmail.send']
            )
            creds = flow.run_local_server(port=8080)
        
        # Guardar las credenciales para la próxima ejecución
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds