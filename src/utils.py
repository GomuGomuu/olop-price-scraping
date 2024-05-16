import unicodedata
import validators
import re


def validate_url(url: str) -> bool:
    return validators.url(url)


def slugify(s):
    normalized = unicodedata.normalize("NFKD", s)
    slug = "".join([c for c in normalized if not unicodedata.combining(c)])
    slug = slug.lower().strip()
    slug = "".join([c if c.isalnum() or c == "-" else " " for c in slug])
    slug = "-".join(slug.split())
    return slug


def extract_float_value(string):
    pattern = r"\d+(?:,\d+)?"
    match = re.search(pattern, string)
    if match:
        matched_number = match.group()
        matched_number = matched_number.replace(",", ".")
        return float(matched_number)
    else:
        return None
