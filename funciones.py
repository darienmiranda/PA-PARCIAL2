from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from config import settings

import re

def send_validate_email(user,title,body):
    message = MIMEMultipart()
    message['subject'] = title
    message['from'] = 'soporte@imagenes-daes.com'#emisor
    message['To'] = user
    message_html = MIMEText(body, 'html')
    message.attach(message_html)
    
    username = settings.SMTP_USERNAME
    password = settings.SMTP_PASSWORD

    server = SMTP(settings.SMTP_HOSTNAME)
    server.starttls()
    server.login(username, password)
    server.sendmail(username, user, message.as_string())

    server.quit()

def validate_mail(correo):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, correo) is not None
