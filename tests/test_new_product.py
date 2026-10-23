import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "new-product.py"


class NewProductTests(unittest.TestCase):
    def run_script(self, stdin):
        return subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=stdin,
            text=True,
            capture_output=True,
            cwd=ROOT,
            timeout=10,
            check=False,
        )

    def test_snippet(self):
        result = self.run_script("19\nmasala chai\nchai\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("if option == 19:", result.stdout)
        self.assertIn('print("masala chai coming up")', result.stdout)
        self.assertIn("chai_no", result.stdout)

    def test_rejects_bad_code(self):
        result = self.run_script("3\nchai\nnot-valid\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("if option ==", result.stdout)

    def test_escapes_quotes(self):
        result = self.run_script('4\nspecial "chef"\nchef\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(r"special \"chef\"", result.stdout)
        self.assertNotIn('print("special "chef"', result.stdout)
