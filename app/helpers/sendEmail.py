import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from os import environ

def sendEmail(receiver_email,uuid):
    sender_email = environ.get("EMAIL", "pepito@gmail.com")
    message = MIMEMultipart("alternative")
    message["Subject"] = "Confirmacion de Email"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    link=environ.get("HOST", "http://localhost:4000/")+uuid
    
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

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    mail_username= environ.get("MAIL_USERNAME", "12344")
    mail_password= environ.get("MAIL_PASSWORD", "12344")
    with smtplib.SMTP("smtp-relay.brevo.com", 587) as server:
        server.login(mail_username, mail_password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )