"""Plain-text email through the standard library. Importing this module does not connect."""

import smtplib
from email.message import EmailMessage

from config import clean_text, env


def smtp_settings():
    sender = clean_text(env("SENDER_EMAIL"), 254)
    password = env("SENDER_PASSWORD")
    recipient = clean_text(env("RECIPIENT_EMAIL"), 254)
    if not sender or not password or not recipient:
        return None
    host = clean_text(env("SMTP_HOST") or "smtp.gmail.com", 253)
    try:
        port = int(env("SMTP_PORT") or "465")
    except ValueError:
        return None
    if not host or port <= 0 or port > 65535:
        return None
    return {
        "sender": sender,
        "password": password,
        "recipient": recipient,
        "host": host,
        "port": port,
    }


def _sanitize_body(body):
    kept = []
    for char in str(body)[:2000]:
        if char in "\n\t":
            kept.append(char)
        elif ord(char) < 32 or ord(char) == 127:
            continue
        else:
            kept.append(char)
    return "".join(kept)


def send_email(subject, body):
    """Return 'sent', 'skipped', or 'failed'. The result never includes secrets."""
    settings = smtp_settings()
    if settings is None:
        return "skipped"
    message = EmailMessage()
    message["Subject"] = clean_text(subject, 120) or "The CLI Restaurant"
    message["From"] = settings["sender"]
    message["To"] = settings["recipient"]
    message.set_content(_sanitize_body(body))
    try:
        _deliver(message, settings)
    except Exception:
        return "failed"
    return "sent"


def _deliver(message, settings):
    host = settings["host"]
    port = settings["port"]
    if port == 465:
        with smtplib.SMTP_SSL(host, port, timeout=20) as smtp:
            smtp.login(settings["sender"], settings["password"])
            smtp.send_message(message)
        return
    with smtplib.SMTP(host, port, timeout=20) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(settings["sender"], settings["password"])
        smtp.send_message(message)
