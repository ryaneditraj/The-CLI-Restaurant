import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "The-Cli-Restaurant.py"


class CliTests(unittest.TestCase):
    def run_cli(self, stdin):
        env = os.environ.copy()
        env.update(
            {
                "SENDER_EMAIL": "",
                "SENDER_PASSWORD": "",
                "RECIPIENT_EMAIL": "",
                "PYTHONIOENCODING": "utf-8",
                "PYTHONUTF8": "1",
            }
        )
        return subprocess.run(
            [sys.executable, str(CLI)],
            input=stdin,
            text=True,
            capture_output=True,
            cwd=ROOT,
            timeout=10,
            env=env,
            check=False,
        )

    def test_menu_and_exit(self):
        result = self.run_cli("12\n99\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("welcome choose your dish", result.stdout)
        self.assertIn("(1)burger", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_order_item(self):
        result = self.run_cli("5\n1\n2\n99\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("burger coming up", result.stdout)
        self.assertIn("burger 2", result.stdout)

    def test_bad_input_does_not_crash(self):
        result = self.run_cli("5\nnope\n99\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Please enter a number from the menu.", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_send_without_config_does_not_pretend_to_send(self):
        result = self.run_cli("5\n1\n1\n0\n99\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Email is not configured.", result.stdout)
        self.assertNotIn("Email sent.", result.stdout)
        self.assertNotIn("Traceback", result.stderr)
