import base64
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from oauth2 import get_oauth2_credentials

def send_email_oauth2(to, subject, message_text):
    creds = get_oauth2_credentials()
    if not creds:
        print("No se pudieron obtener las credenciales. Por favor, autoriza la aplicación.")
        return

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = MIMEText(message_text)
        message['to'] = to
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        body = {'raw': raw_message}
        message = service.users().messages().send(userId='me', body=body).execute()
        print(f'Mensaje enviado: {message["id"]}')
    except Exception as e:
        print(f'Ocurrió un error al enviar el correo: {str(e)}')