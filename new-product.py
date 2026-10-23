#!/usr/bin/env python3
"""Print a menu-item snippet for The-Cli-Restaurant.py. It does not edit that file."""

import re

from config import clean_text


def python_string(value):
    return clean_text(value, 80).replace("\\", "\\\\").replace('"', '\\"')


def main():
    try:
        raw_no = input("Product no>")
    except EOFError:
        raise SystemExit(1)
    if not re.fullmatch(r"[0-9]{1,4}", raw_no.strip()):
        print("Product no must be a number.")
        raise SystemExit(1)
    try:
        product = python_string(input("product name>"))
        product_code = input("Product code>").strip()
    except EOFError:
        raise SystemExit(1)
    if not product:
        print("Product name cannot be empty.")
        raise SystemExit(1)
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", product_code):
        print(
            "Product code must be a Python identifier made of letters, digits, and underscores."
        )
        raise SystemExit(1)
    number = int(raw_no)
    template = f"""
if option == {number}:
        print("{product} coming up")
        {product_code}_no = str(input("How Many: "))
        items = (hitems+","+"{product} "+{product_code}_no)
        print(items)
        hitems = items"""
    print(template)
    print("Review this snippet before pasting it into The-Cli-Restaurant.py.")


if __name__ == "__main__":
    main()
