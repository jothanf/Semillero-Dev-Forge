
import os
from send_mail_oauth2 import send_email_oauth2

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Solo para desarrollo local

recipient_email = 'jothanferney@gmail.com'
subject = 'Prueba de Envío de Correo'
message_text = 'Este es un mensaje de prueba enviado desde el script de OAuth2.'

send_email_oauth2(recipient_email, subject, message_text)