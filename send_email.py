import smtplib, ssl
from email.message import EmailMessage
from constants import *

"""Implementing Email sending function"""
def send_email(subject: str, body: str):
    host = SMTP_HOST
    port = SMTP_PORT
    user = SMTP_USER
    pwd  = SMTP_PASS
    sender = ALERT_SENDER
    recipient = ALERT_RECIPIENT

    if not (host and port and sender and recipient):
        raise RuntimeError("SMTP env vars missing (need host, port, sender, recipient).")

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP(host, port, timeout=20) as server:
        server.starttls(context=context)
        if user:
            server.login(user, pwd or "")
        server.send_message(msg)

