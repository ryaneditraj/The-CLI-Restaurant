#!/usr/bin/env python3
"""Flask table-reservation site for The CLI Restaurant."""

import re
import secrets
from collections import defaultdict
from pathlib import Path
from time import time
from xml.sax.saxutils import escape

from flask import Flask, abort, g, render_template, request, session

from config import clean_text, env
from mailer import send_email
from seo import DESCRIPTION, FAQS, KEYWORDS, structured_data

ROOT = Path(__file__).resolve().parent
PHONE_PATTERN = re.compile(r"[0-9+\-() .]{3,32}")
MAX_BOOKINGS_PER_WINDOW = 8
RATE_WINDOW_SECONDS = 60
_booking_hits = defaultdict(list)

app = Flask(__name__)
app.config["SECRET_KEY"] = env("SECRET_KEY") or secrets.token_hex(32)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = env("SITE_URL").startswith("https://")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024


def _hostname():
    raw = request.host or ""
    if raw.startswith("["):
        end = raw.find("]")
        if end != -1:
            return raw[1:end]
    return raw.split(":")[0]


def site_url():
    configured = env("SITE_URL").rstrip("/")
    if configured:
        if any(char in configured for char in "\r\n\t <>\"'"):
            return ""
        return configured
    if _hostname() in {"127.0.0.1", "localhost", "::1"}:
        return request.host_url.rstrip("/")
    return ""


@app.context_processor
def inject_template_globals():
    current_site = site_url()
    return {
        "site_url": current_site,
        "csp_nonce": getattr(g, "csp_nonce", ""),
        "csrf_token": session.get("_csrf_token", ""),
        "description": DESCRIPTION,
        "keywords": KEYWORDS,
        "faqs": FAQS,
        "structured_data": structured_data(current_site),
    }


@app.before_request
def prepare_request():
    g.csp_nonce = secrets.token_urlsafe(16)
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_urlsafe(32)


@app.after_request
def add_security_headers(response):
    nonce = getattr(g, "csp_nonce", "")
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        f"script-src 'self' 'nonce-{nonce}'; "
        "style-src 'self' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none'"
    )
    response.headers.pop("Server", None)
    if request.method == "POST":
        response.headers["Cache-Control"] = "no-store"
    return response


def rate_limited(ip):
    now = time()
    hits = [
        stamp
        for stamp in _booking_hits.get(ip, [])
        if now - stamp < RATE_WINDOW_SECONDS
    ]
    limited = len(hits) >= MAX_BOOKINGS_PER_WINDOW
    if not limited:
        hits.append(now)
    if hits:
        _booking_hits[ip] = hits
    elif ip in _booking_hits:
        del _booking_hits[ip]
    if len(_booking_hits) > 1000:
        stale = [
            key
            for key, stamps in _booking_hits.items()
            if not any(now - stamp < RATE_WINDOW_SECONDS for stamp in stamps)
        ]
        for key in stale:
            del _booking_hits[key]
    return limited


def valid_phone(mobile):
    return PHONE_PATTERN.fullmatch(mobile) is not None and sum(
        char.isdigit() for char in mobile
    ) >= 3


def csrf_ok():
    expected = session.get("_csrf_token", "")
    sent = request.form.get("csrf_token", "")
    if not expected or not sent:
        return False
    return secrets.compare_digest(expected, sent)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if not csrf_ok():
        return (
            render_template(
                "index.html",
                error="The form expired. Please submit it again.",
            ),
            400,
        )

    name = clean_text(request.form.get("name", ""), 120)
    mobile = clean_text(request.form.get("mobilenumber", ""), 32)
    party = clean_text(request.form.get("numberpers", ""), 16)
    if not name or not mobile or not party:
        return (
            render_template(
                "index.html",
                error="Name, mobile number, and party size are required.",
            ),
            400,
        )
    if not valid_phone(mobile):
        return (
            render_template(
                "index.html",
                error="Enter a mobile number using digits and + - ( ) or spaces.",
            ),
            400,
        )

    if rate_limited(request.remote_addr or "unknown"):
        return (
            render_template(
                "index.html",
                error="Too many reservations from this network. Please wait a minute and try again.",
            ),
            429,
        )

    result = send_email(
        subject="New table reservation",
        body=(
            f"Name: {name}\n"
            f"Mobile Number: {mobile}\n"
            f"Number of people: {party}\n"
        ),
    )
    if result == "failed":
        app.logger.error("Reservation email failed")
        return (
            render_template(
                "submitted.html",
                heading="We could not send the reservation. Please try again in a moment.",
            ),
            502,
        )
    if result == "skipped":
        app.logger.warning(
            "Reservation accepted without email because SMTP is not configured"
        )
    session["_csrf_token"] = secrets.token_urlsafe(32)
    return render_template("submitted.html", name=name)


@app.route("/email", methods=["GET", "POST"])
def email():
    """Local test hook. GET does not send mail."""
    if request.method == "GET":
        return "POST to this endpoint from localhost to send a test email.\n"
    if (request.remote_addr or "") not in {"127.0.0.1", "::1"}:
        abort(403)
    result = send_email(
        subject="The CLI Restaurant test",
        body="Test message from The CLI Restaurant.",
    )
    if result == "skipped":
        return "Email is not configured.\n", 503
    if result == "failed":
        app.logger.error("Test email failed")
        return "Could not send email.\n", 502
    return render_template("index.html")


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    return "not available"


@app.get("/robots.txt")
def robots():
    text = (ROOT / "robots.txt").read_text(encoding="utf-8").rstrip() + "\n"
    base = site_url()
    if base and "Sitemap:" not in text:
        text += f"\nSitemap: {base}/sitemap.xml\n"
    return app.response_class(text, mimetype="text/plain; charset=utf-8")


@app.get("/sitemap.xml")
def sitemap():
    base = site_url()
    if not base:
        abort(404)
    urls = "\n".join(
        f"  <url><loc>{escape(base + path)}</loc></url>" for path in ("/", "/sign-up")
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n"
        "</urlset>\n"
    )
    return app.response_class(xml, mimetype="application/xml")


@app.get("/llms.txt")
def llms():
    text = (ROOT / "llms.txt").read_text(encoding="utf-8")
    return app.response_class(text, mimetype="text/plain; charset=utf-8")


@app.get("/.well-known/security.txt")
def security_txt():
    text = (ROOT / ".well-known" / "security.txt").read_text(encoding="utf-8")
    return app.response_class(text, mimetype="text/plain; charset=utf-8")


def main():
    try:
        port = int(env("PORT") or "5000")
    except ValueError as exc:
        raise SystemExit("PORT must be a number.") from exc
    debug = env("FLASK_DEBUG") == "1"
    if debug:
        app.logger.warning(
            "FLASK_DEBUG=1 enables the interactive debugger. Keep it off on any shared or public host."
        )
    app.run(debug=debug, host=env("HOST") or "127.0.0.1", port=port)


if __name__ == "__main__":
    main()
