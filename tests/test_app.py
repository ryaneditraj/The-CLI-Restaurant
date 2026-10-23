import os
import unittest
from pathlib import Path

os.environ["SENDER_EMAIL"] = ""
os.environ["SENDER_PASSWORD"] = ""
os.environ["RECIPIENT_EMAIL"] = ""

import app as mail_demo

ROOT = Path(__file__).resolve().parents[1]


class FlaskMailDemoTests(unittest.TestCase):
    def setUp(self):
        os.environ["SENDER_EMAIL"] = ""
        os.environ["SENDER_PASSWORD"] = ""
        os.environ["RECIPIENT_EMAIL"] = ""
        self.client = mail_demo.app.test_client()

    def test_unconfigured_does_not_send(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 503)
        self.assertIn(b"not configured", response.data)

    def test_source_has_no_password_literal(self):
        text = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertNotIn("*****", text)
        self.assertNotRegex(text, r"MAIL_PASSWORD['\"]\]\s*=\s*['\"]")
