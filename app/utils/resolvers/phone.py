import re
from typing import Literal

# Burmese unicode ranges
BURMESE_CHAR_PATTERN = re.compile(r'[\u1000-\u109F\uAA60-\uAA7F\uA9E0-\uA9FF]')

# English alphabet pattern
ENGLISH_CHAR_PATTERN = re.compile(r'[a-zA-Z]')

# Burmese digit translation map
BURMESE_DIGITS = {
    '၀': '0', '၁': '1', '၂': '2', '၃': '3', '၄': '4',
    '၅': '5', '၆': '6', '၇': '7', '၈': '8', '၉': '9'
}


def normalize_to_ascii_digits(text: str) -> str:
    """Converts Burmese numerical digits (၀-၉) to ASCII digits (0-9)."""
    return "".join(BURMESE_DIGITS.get(char, char) for char in text)


def is_phone_number(text: str) -> bool:
    """
    Detects if the input text represents a valid phone number.
    Supports both English (09...) and Burmese (၀၉...) digits, 
    international codes (+95...), and standard spaces/hyphens.
    """
    if not text:
        return False

    # 1. Convert Burmese digits to ASCII
    normalized = normalize_to_ascii_digits(text.strip())

    # 2. Strip formatting spaces, hyphens, and parentheses
    cleaned = re.sub(r'[\s\-\(\)]', '', normalized)

    # 3. Check Myanmar / Global phone number formats:
    #    - Domestic format: 09XXXXXXXX (7 to 9 digits after 09)
    #    - International format: +959XXXXXXXX or 959XXXXXXXX
    #    - Generic standard 7-15 digit string starting with + or digits
    mm_phone_pattern = r'^(?:\+?959|09)\d{7,9}$'
    generic_phone_pattern = r'^\+?\d{7,15}$'

    return bool(re.match(mm_phone_pattern, cleaned) or re.match(generic_phone_pattern, cleaned))


def classify_text(text: str) -> Literal["phone_number", "burmese", "english", "mixed", "numeric", "unknown"]:
    """
    Classifies the input string into one of:
    - 'phone_number': Valid phone format (e.g. '09123456789', '၀၉၇၉...')
    - 'burmese': Text containing Burmese characters/words
    - 'english': Text containing English alphabet characters/words
    - 'mixed': Contains both Burmese and English words
    - 'numeric': Plain numbers (not recognized as phone numbers)
    - 'unknown': Empty or non-alphanumeric punctuation
    """
    if not text or not text.strip():
        return "unknown"

    raw_text = text.strip()

    # Step 1: Check for phone number pattern first
    if is_phone_number(raw_text):
        return "phone_number"

    # Step 2: Check character composition
    has_burmese = bool(BURMESE_CHAR_PATTERN.search(raw_text))
    has_english = bool(ENGLISH_CHAR_PATTERN.search(raw_text))

    if has_burmese and has_english:
        return "mixed"
    if has_burmese:
        return "burmese"
    if has_english:
        return "english"

    # Step 3: Check if pure numeric (non-phone)
    normalized_digits = normalize_to_ascii_digits(raw_text)
    if normalized_digits.isdigit():
        return "numeric"

    return "unknown"