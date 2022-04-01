from email import message
from http import server
from smtplib import SMTP
from email.message import EmailMessage
from config import settings

message = EmailMessage()

message['subject'] = 'Este es el asunto'
message['from'] = 'jamescordoba2020@gmail.com'#emisor
message['To'] = 'cordobstiven71@gmail.com'#receptor
message.set_content('Este es un email de pruebas')

username = settings.SMTP_HOSTNAME
password = settings.SMTP_PASSWORD

server = SMTP(settings.SMTP_HOSTNAME)
server.starttls()
server.login(username, password)
server.send_message(message)

server.quit()