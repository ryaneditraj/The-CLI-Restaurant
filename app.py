#!/usr/bin/env python3
"""Optional Flask-Mail demo.

The table-booking site is server.py. This file sends one test message when
SENDER_EMAIL, SENDER_PASSWORD, and RECIPIENT_EMAIL are set.
"""

from flask import Flask
from flask_mail import Mail, Message

from config import env

app = Flask(__name__)


def _smtp_port():
    try:
        return int(env("SMTP_PORT") or "465")
    except ValueError:
        return 465


def configure_mail(flask_app):
    port = _smtp_port()
    flask_app.config["MAIL_SERVER"] = env("SMTP_HOST") or "smtp.gmail.com"
    flask_app.config["MAIL_PORT"] = port
    flask_app.config["MAIL_USERNAME"] = env("SENDER_EMAIL")
    flask_app.config["MAIL_PASSWORD"] = env("SENDER_PASSWORD")
    flask_app.config["MAIL_USE_SSL"] = port == 465
    flask_app.config["MAIL_USE_TLS"] = port != 465
    flask_app.config["MAIL_DEFAULT_SENDER"] = env("SENDER_EMAIL")
    return Mail(flask_app)


mail = configure_mail(app)


@app.get("/")
def index():
    sender = env("SENDER_EMAIL")
    password = env("SENDER_PASSWORD")
    recipient = env("RECIPIENT_EMAIL")
    if not sender or not password or not recipient:
        return (
            "Email is not configured. Copy .env.example to .env and set "
            "SENDER_EMAIL, SENDER_PASSWORD, and RECIPIENT_EMAIL.\n",
            503,
        )
    message = Message(
        subject="Hello",
        sender=sender,
        recipients=[recipient],
        body="Hello Flask message sent from Flask-Mail",
    )
    try:
        mail.send(message)
    except Exception:
        app.logger.error("Flask-Mail could not send the test message")
        return ("Could not send email.\n", 502)
    return "Sent"


def main():
    try:
        port = int(env("PORT") or "5000")
    except ValueError as exc:
        raise SystemExit("PORT must be a number.") from exc
    app.run(
        debug=env("FLASK_DEBUG") == "1",
        host=env("HOST") or "127.0.0.1",
        port=port,
    )


if __name__ == "__main__":
    main()
