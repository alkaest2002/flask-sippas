from flask_mail import Message

from flaskApp import app
from flaskApp.extensions.mail_ext import mail
from .decorators import asynchronous

@asynchronous
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    
    # compose
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    
    # send
    send_async_email(app, msg)