# Contributing to The CLI Restaurant

Thanks for looking at the project. Issues and pull requests are welcome.

## Ground rules

- Be kind. The [Code of Conduct](CODE_OF_CONDUCT.md) applies to issues, pull requests, and discussions.
- Do not commit `.env` files, mailbox passwords, or API keys.
- Keep pull requests focused. A bug fix and a redesign should be two pull requests.
- The terminal menu and the booking form should keep working for the happy path: order a dish, or submit a name, mobile number, and party size.

## Set up

```bash
git clone https://github.com/ryaneditraj/The-CLI-Restaurant.git
cd The-CLI-Restaurant
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

On Windows, activate the virtual environment with `.venv\Scripts\activate`.

## Run

```bash
python server.py
python The-Cli-Restaurant.py
```

The booking site listens on `http://127.0.0.1:5000`. Email stays off until `.env` has `SENDER_EMAIL`, `SENDER_PASSWORD`, and `RECIPIENT_EMAIL`.

## Tests

```bash
python -m unittest discover -s tests -v
```

The tests do not contact a real mail server.

## Project notes

- `server.py` is the booking website. `The-Cli-Restaurant.py` is the terminal order pad. `app.py` is a separate Flask-Mail demo.
- `new-product.py` only prints a snippet. Paste it into the terminal menu yourself after you read it.
- Guest names are rendered by Jinja, which escapes HTML. Keep it that way.
- `python server.py` is a local development server. A public host should run the app with a WSGI server and `FLASK_DEBUG` left at `0`.

## Pull requests

1. Open an issue for a large change before you write it.
2. Add or update a test when you change request handling, email, or the menu loop.
3. Run the unit tests.
4. Fill in the pull request template.
