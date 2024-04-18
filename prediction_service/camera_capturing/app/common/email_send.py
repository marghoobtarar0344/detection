

import smtplib, ssl
from email.message import EmailMessage

from config.global_variables import (
    SMTP_PORT,
    SMTP_SERVER,
    SENDER_EMAIL,
    RECIEVER_EMAIL,
    EMAIL_ACCOUNT_PASSWORD
)


port = SMTP_PORT  # For starttls
smtp_server = SMTP_SERVER
sender_email = SENDER_EMAIL
receiver_email = RECIEVER_EMAIL.split(',')
password = EMAIL_ACCOUNT_PASSWORD

def email_notification(content,message_type):
    try:
        msg = EmailMessage()
        msg['Subject'] = f'Bushfire Notification ({message_type})'
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg.set_content(str(content))

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print('error in email sending',e)
    else:
        return 'email sending successful'
