# Security policy

## Reporting a vulnerability

Please report vulnerabilities privately through
[GitHub security advisories](https://github.com/ryaneditraj/The-CLI-Restaurant/security/advisories/new).

Do not open a public issue for a security report, and do not paste live mailbox
passwords or guest phone numbers into a report.

The maintainer will review private reports. Give them a chance to fix the issue
before any public disclosure.

## Supported code

| Version | Supported |
| --- | --- |
| `main` | Yes |
| Older commits | No |

## Credential that was committed

Commit `e2b8b1afdadee1ef76c5901007106377e042d94f` (6 May 2022) stored a personal
mailbox address and password in `server.py`. Commit
`d297e4bf8c63cad64a48757f7dfc2579a4d7b04b` replaced them with placeholders, but
the original values are still in git history. The same first commit also stored
a Flask `SECRET_KEY` literal, which stayed in the working tree until the
environment-variable change.

This project does not rewrite history. If you maintain the repository, rotate
that mailbox password, turn on two-factor authentication, and stop using the
old Flask secret. The current code reads mail settings and `SECRET_KEY` from
the environment. See `.env.example`.

## What the app does with guest data

The booking form collects a name, a mobile number, and a party size.

- The confirmation page shows the name. Jinja escapes it.
- When `SENDER_EMAIL`, `SENDER_PASSWORD`, and `RECIPIENT_EMAIL` are set, those
  three fields are emailed as plain text over TLS.
- There is no database. Restarting the app drops the in-memory rate-limit
  counters and the process-local signing key (unless `SECRET_KEY` is set).

## Hardening in the current code

- No mailbox password or API key in the working tree.
- The process does not open an SMTP connection on import.
- `FLASK_DEBUG` defaults off. The debugger is remote-code-execution if it is
  exposed.
- The development server binds to `127.0.0.1` unless `HOST` is set.
- Reservation posts need the cookie token from the form.
- Control characters are stripped before they reach mail headers or the page.
- `/email` does not send on GET, and POST is limited to localhost.
- Responses set `Content-Security-Policy`, `X-Content-Type-Options`,
  `X-Frame-Options`, and `Referrer-Policy`.
- Booking posts are limited to eight per minute per address, in memory.
- Request bodies are capped at 16 KB.
- Dependencies are pinned in `requirements.txt`. Dependabot opens update
  pull requests.

## Residual risk

- Git history still contains the old mailbox password until someone rewrites
  history on purpose. Rotation matters more than a rewrite.
- The rate limit is per process and resets on restart. There is no CAPTCHA.
- `HOST=0.0.0.0` or `FLASK_DEBUG=1` on a shared network is unsafe.
- `python server.py` is Werkzeug's development server, not a production server.
- A reverse proxy that does not overwrite the client address shares one rate
  limit across visitors. The app does not trust `X-Forwarded-For`.
- `new-product.py` prints Python for you to paste. Read it before pasting.
- `templates/sign-up copy.html` and `submited.html` are unused drafts.
- The hero looks for `static/pic.jpg`. That file was never in the repository.
