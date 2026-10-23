"""Environment helpers. A local .env file never overrides real variables."""

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")


def load_dotenv(path=None):
    env_path = Path(path) if path else ROOT / ".env"
    if not env_path.is_file():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        if key:
            os.environ.setdefault(key, value)


def env(name, default=""):
    return os.environ.get(name, default).strip()


def clean_text(value, limit=120):
    """Drop control characters, trim, and cap length. Safe for headers and HTML text."""
    if value is None:
        return ""
    return _CONTROL.sub("", str(value)).strip()[:limit]


load_dotenv()
