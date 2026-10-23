import os
import re
import unittest
from pathlib import Path
from unittest.mock import patch

import server
from seo import FAQS

ROOT = Path(__file__).resolve().parents[1]


class BookingSiteTests(unittest.TestCase):
    def setUp(self):
        self._clear_mail_env()
        server._booking_hits.clear()
        self.client = server.app.test_client()

    def tearDown(self):
        self._clear_mail_env()
        server._booking_hits.clear()

    def _clear_mail_env(self):
        for key in (
            "SENDER_EMAIL",
            "SENDER_PASSWORD",
            "RECIPIENT_EMAIL",
            "SMTP_HOST",
            "SMTP_PORT",
            "SITE_URL",
        ):
            os.environ.pop(key, None)

    def post_booking(self, **overrides):
        home = self.client.get("/")
        match = re.search(
            r'name="csrf_token" value="([^"]+)"',
            home.get_data(as_text=True),
        )
        self.assertIsNotNone(match)
        data = {
            "csrf_token": match.group(1),
            "name": "Ada",
            "mobilenumber": "555-0100",
            "numberpers": "2",
        }
        data.update(overrides)
        return self.client.post("/", data=data)

    def test_homepage_has_form_faq_and_seo(self):
        response = self.client.get("/")
        body = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("The CLI Restaurant", body)
        self.assertIn("Table reservation", body)
        self.assertIn('name="csrf_token"', body)
        self.assertNotIn("<style", body.lower())
        for item in FAQS:
            self.assertIn(item["question"], body)
            self.assertIn(item["answer"], body)
        self.assertIn("SoftwareApplication", body)
        self.assertIn("FAQPage", body)
        self.assertIn("Ryan Editraj", body)
        self.assertIn("og:title", body)
        self.assertIn("og-cover.png", body)
        nonce = re.search(r'nonce="([^"]+)"', body).group(1)
        self.assertIn(f"nonce-{nonce}", response.headers["Content-Security-Policy"])
        policy = response.headers["Content-Security-Policy"]
        self.assertNotIn("unsafe-inline", policy)
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertNotIn("Server", response.headers)

    def test_get_does_not_open_smtp(self):
        with patch("mailer.smtplib.SMTP_SSL") as smtp:
            self.client.get("/")
            smtp.assert_not_called()

    def test_booking_escapes_html_and_skips_mail_when_unconfigured(self):
        with patch("mailer.smtplib.SMTP_SSL") as smtp:
            response = self.post_booking(name="<script>alert(1)</script>")
        smtp.assert_not_called()
        body = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("<script>alert", body)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", body)
        self.assertIn("Please expect a call from us shortly.", body)

    def test_missing_csrf_is_rejected(self):
        response = self.client.post(
            "/",
            data={"name": "Ada", "mobilenumber": "555-0100", "numberpers": "2"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertNotIn(b"expect a call", response.data)

    def test_bad_phone_is_rejected(self):
        response = self.post_booking(mobilenumber="call me")
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"mobile number", response.data)

    def test_header_injection_stays_in_the_body(self):
        os.environ["SENDER_EMAIL"] = "desk@example.com"
        os.environ["SENDER_PASSWORD"] = "app-password"
        os.environ["RECIPIENT_EMAIL"] = "kitchen@example.com"
        with patch("mailer.smtplib.SMTP_SSL") as smtp_cls:
            connection = smtp_cls.return_value.__enter__.return_value
            response = self.post_booking(name="Ada\r\nBcc: evil@example.com")
        self.assertEqual(response.status_code, 200)
        connection.login.assert_called_once_with("desk@example.com", "app-password")
        message = connection.send_message.call_args[0][0]
        self.assertEqual(message["To"], "kitchen@example.com")
        self.assertIsNone(message["Bcc"])
        self.assertNotIn("\n", message["Subject"])
        content = message.get_content()
        self.assertNotIn("\r", content)
        self.assertNotIn("app-password", content)
        self.assertIn("Ada", content)
        self.assertIn("555-0100", content)

    def test_mail_failure_does_not_leak_or_confirm(self):
        os.environ["SENDER_EMAIL"] = "desk@example.com"
        os.environ["SENDER_PASSWORD"] = "app-password"
        os.environ["RECIPIENT_EMAIL"] = "kitchen@example.com"
        with patch("mailer.smtplib.SMTP_SSL") as smtp_cls:
            connection = smtp_cls.return_value.__enter__.return_value
            connection.login.side_effect = OSError("mailbox said nope")
            response = self.post_booking()
        self.assertEqual(response.status_code, 502)
        self.assertNotIn(b"expect a call", response.data)
        self.assertNotIn(b"nope", response.data)
        self.assertNotIn(b"app-password", response.data)

    def test_rate_limit(self):
        original = server.MAX_BOOKINGS_PER_WINDOW
        server.MAX_BOOKINGS_PER_WINDOW = 2
        self.addCleanup(setattr, server, "MAX_BOOKINGS_PER_WINDOW", original)
        self.assertEqual(self.post_booking().status_code, 200)
        self.assertEqual(self.post_booking(name="Bea").status_code, 200)
        blocked = self.post_booking(name="Cy")
        self.assertEqual(blocked.status_code, 429)

    def test_sign_up_stub(self):
        self.assertEqual(self.client.get("/sign-up").get_data(as_text=True), "not available")
        self.assertEqual(self.client.post("/sign-up").get_data(as_text=True), "not available")

    def test_email_get_does_not_send(self):
        with patch("mailer.smtplib.SMTP_SSL") as smtp:
            response = self.client.get("/email")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"POST", response.data)
        smtp.assert_not_called()

    def test_email_post_is_local_only(self):
        response = self.client.post(
            "/email",
            environ_overrides={"REMOTE_ADDR": "203.0.113.5"},
        )
        self.assertEqual(response.status_code, 403)

    def test_email_post_without_config(self):
        response = self.client.post("/email")
        self.assertEqual(response.status_code, 503)

    def test_discovery_files(self):
        robots = self.client.get("/robots.txt")
        self.assertEqual(robots.status_code, 200)
        self.assertIn(b"Allow: /", robots.data)
        self.assertIn(b"Sitemap: http://localhost/sitemap.xml", robots.data)
        sitemap = self.client.get("/sitemap.xml")
        self.assertIn(b"http://localhost/sign-up", sitemap.data)
        llms = self.client.get("/llms.txt")
        self.assertIn(b"Ryan Editraj", llms.data)
        security = self.client.get("/.well-known/security.txt")
        self.assertIn(b"Contact:", security.data)
        css = self.client.get("/static/styles.css")
        self.assertEqual(css.status_code, 200)
        self.assertIn(b"Oleo Script", css.get_data())
        css.close()
        cover = self.client.get("/static/og-cover.png")
        self.assertEqual(cover.status_code, 200)
        self.assertTrue(cover.get_data().startswith(b"\x89PNG"))
        cover.close()

    def test_sources_have_no_hardcoded_secrets(self):
        for name in ("server.py", "mailer.py", "The-Cli-Restaurant.py", "config.py"):
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertNotIn("senderpass", text)
            self.assertNotIn("*****", text)
            self.assertNotRegex(text, r"sender_pass\s*=\s*['\"]")
            self.assertNotRegex(text, r"SECRET_KEY['\"]\]\s*=\s*['\"]")
