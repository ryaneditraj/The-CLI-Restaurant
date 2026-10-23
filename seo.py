"""Copy and structured data shared by the booking page."""

import json

DESCRIPTION = (
    "The CLI Restaurant is a free open-source Python project: a command-line "
    "restaurant order pad and a Flask table reservation website."
)

KEYWORDS = (
    "open source CLI restaurant, Python restaurant management system, "
    "command-line food ordering, Flask table reservation, table booking website, "
    "terminal point of sale"
)

FAQS = [
    {
        "question": "How do I reserve a table?",
        "answer": (
            "Enter your name, mobile number, and party size, then submit the form. "
            "The next page confirms the request. When email is configured, the same "
            "details are sent to the restaurant."
        ),
    },
    {
        "question": "Does The CLI Restaurant store my phone number?",
        "answer": (
            "This demo does not use a database. Your name and mobile number appear "
            "on the confirmation page and, when email is configured, in a message "
            "to the restaurant. Nothing else is saved."
        ),
    },
    {
        "question": "What does the command-line menu do?",
        "answer": (
            "Staff run The-Cli-Restaurant.py, pick dishes for a table, and email "
            "that order to the kitchen or the front desk."
        ),
    },
    {
        "question": "Who made The CLI Restaurant?",
        "answer": (
            "Ryan Editraj, an AI builder and tech creator. The project is MIT "
            "licensed and the source is on GitHub."
        ),
    },
]


def _dump(data):
    serialized = json.dumps(data, ensure_ascii=False)
    return (
        serialized.replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )


def structured_data(site_url=""):
    blocks = [
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "The CLI Restaurant",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Windows, macOS, Linux",
            "description": DESCRIPTION,
            "url": "https://github.com/ryaneditraj/The-CLI-Restaurant",
            "license": "https://opensource.org/licenses/MIT",
            "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "author": {
                "@type": "Person",
                "name": "Ryan Editraj",
                "url": "https://github.com/ryaneditraj",
                "sameAs": [
                    "https://github.com/ryaneditraj",
                    "https://instagram.com/ryaneditraj",
                ],
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item["question"],
                    "acceptedAnswer": {"@type": "Answer", "text": item["answer"]},
                }
                for item in FAQS
            ],
        },
    ]
    if site_url:
        blocks.append(
            {
                "@context": "https://schema.org",
                "@type": "WebSite",
                "name": "The CLI Restaurant",
                "url": site_url,
                "description": DESCRIPTION,
                "inLanguage": "en",
            }
        )
    return [_dump(block) for block in blocks]
