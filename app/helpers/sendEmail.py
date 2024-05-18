import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from os import environ

def sendEmail(receiver_email,uuid, link):
    sender_email = os.getenv("EMAIL")
    message = MIMEMultipart("alternative")
    message["Subject"] = "Confirmacion de Email"
    message["From"] = sender_email
    message["To"] = receiver_email

    
    link=link +"/confirmEmail/"+uuid
    
    text = f"""\
        Hola,
        este correo se registro recientemente en ________ .
        Si es usted quien se registro por favor ingrese en el siguiente link
        {link}
        Si no ingresa en el link en el plazo de 24 horas de la creación de la cuenta, esta sera eliminada.
"""
    html = f"""\
    <html>
    <body>
        <p>Hola,<br>
        este correo se registro recientemente en ________ .<br>
        Si es usted quien se registro por favor haga click en el siguiente enlace <br>
        <a href="{link}">Confirmación de Email</a> 
        Si no puede ingresar por favor ingrese al siguiente link <br>
        {link} <br>
        Si no ingresa en el link en el plazo de 24 horas de la creación de la cuenta, esta sera eliminada.
        </p>
        La cuenta del remitente es una cuenta creada para hacer pruebas
    </body>
    </html>
    """

    
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

   
    message.attach(part1)
    message.attach(part2)

    mail_username = os.getenv("MAIL_USERNAME")
    mail_password = os.getenv("MAIL_PASSWORD")
    for i in range(1, 1001):
        print(mail_username)
    with smtplib.SMTP("smtp-relay.brevo.com", 587) as server:
        server.login(mail_username, mail_password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )