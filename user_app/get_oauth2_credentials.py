import os
import pickle
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request

def get_oauth2_credentials():
    creds = None
    # Cargar credenciales existentes si ya existen
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Si no hay credenciales o son inválidas, se inicia el flujo de OAuth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Inicia el flujo de autorización OAuth
            flow = Flow.from_client_secrets_file(
                os.path.join(os.getcwd(), 'credentials.json'),
                scopes=['https://www.googleapis.com/auth/gmail.send']
            )

            # Aquí no necesitamos redirigir a localhost, simplemente generamos la URL
            flow.redirect_uri = 'http://localhost:8000/oauth2callback/'

            # Genera la URL de autorización
            authorization_url, _ = flow.authorization_url(
                access_type='offline', 
                include_granted_scopes='true'
            )
            print(f'Por favor visite esta URL para autorizar la aplicación: {authorization_url}')

            # Aquí puedes ingresar el código manualmente después de la autorización
            authorization_code = input('Introduce el código de autorización: ')

            # Intercambia el código por las credenciales
            flow.fetch_token(code=authorization_code)
            creds = flow.credentials

    # Guardar las credenciales en el archivo token.pickle
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
    
    return creds

# Llamar a la función para obtener credenciales
get_oauth2_credentials()
