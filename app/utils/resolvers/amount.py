import re
from typing import Optional, Union

# Burmese digit translation map
BURMESE_DIGITS = {
    '၀': '0', '၁': '1', '၂': '2', '၃': '3', '၄': '4',
    '၅': '5', '၆': '6', '၇': '7', '၈': '8', '၉': '9'
}

# Burmese word-to-number mapping (includes all spelling variations)
BURMESE_WORDS = {
    'တစ်': 1, 'တ': 1, '၁': 1,
    'နှစ်': 2, '၂': 2,
    'သုံး': 3, '၃': 3,
    'လေး': 4, '၄': 4,
    'ငါး': 5, '၅': 5,
    'ခြောက်': 6, '၆': 6,
    'ခုနှစ်': 7, 'ခုနစ်': 7, 'ခွန်': 7, '၇': 7,
    'ရှစ်': 8, '၈': 8,
    'ကိုး': 9, '၉': 9,
    'ဆယ်': 10, 'ဆယ့်': 10, '၁၀': 10
}

# Unit multipliers ORDERED from largest to smallest
BURMESE_UNITS = [
    ('ကုဋေ', 10000000),
    ('သန်း', 1000000),
    ('သိန်း', 100000),
    ('သောင်း', 10000),
    ('ထောင်', 1000),
    ('ရာ', 100),
]


def normalize_burmese_digits(text: str) -> str:
    """Converts Burmese numerical digits (၀-၉) to English ASCII digits (0-9)."""
    return "".join(BURMESE_DIGITS.get(char, char) for char in text)


def parse_burmese_prefix(prefix: str) -> float:
    """
    Parses prefix words like 'ခုနစ်', 'ဆယ့်ငါး', '၁၅', or 'ငါး' into an integer/float.
    """
    prefix = prefix.strip()
    if not prefix:
        return 1.0

    # 1. Direct word match
    if prefix in BURMESE_WORDS:
        return float(BURMESE_WORDS[prefix])

    # 2. Try converting Burmese digits
    clean_prefix = normalize_burmese_digits(prefix)
    if clean_prefix.isdigit():
        return float(clean_prefix)

    # 3. Handle compound word prefixes (e.g., 'ဆယ့်ငါး' = 15, 'ဆယ့်ရှစ်' = 18)
    if 'ဆယ့်' in prefix or 'ဆယ်' in prefix:
        parts = re.split(r'ဆယ့်|ဆယ်', prefix)
        tens_part = 10
        units_part = 0
        if len(parts) > 1 and parts[1]:
            unit_word = parts[1].strip()
            units_part = BURMESE_WORDS.get(unit_word, 0)
        return float(tens_part + units_part)

    return 1.0


def resolve_burmese_amount(val: Optional[Union[str, int, float]]) -> Optional[str]:
    """
    Parses Burmese currency and numerical amounts into standard ASCII integer strings.
    Handles all spelling variations, compounds, digits, multipliers, and half-units ('ခွဲ').
    """
    if val is None:
        return None

    raw = str(val).strip()
    if not raw:
        return None

    # Step 1: Handle simple numeric string or converted Burmese digits
    converted_digits = normalize_burmese_digits(raw)
    if converted_digits.isdigit():
        return str(int(converted_digits))

    # Clean text input (remove spaces, connectors '့', and common suffixes like 'ကျပ်')
    text = raw.replace(" ", "").replace("ကျပ်", "").replace("့", "")

    # Check for half-unit modifier 'ခွဲ' (e.g., ခုနစ်သောင်းခွဲ = 70,000 + 5,000 = 75,000)
    has_half = 'ခွဲ' in text
    if has_half:
        text = text.replace('ခွဲ', '')

    multiplier = 1
    matched_unit = None

    # Detect unit multiplier in strictly ordered array
    for unit_name, unit_val in BURMESE_UNITS:
        if unit_name in text:
            matched_unit = unit_name
            multiplier = unit_val
            break

    if matched_unit:
        prefix = text.split(matched_unit)[0].strip()
        base_val = parse_burmese_prefix(prefix)

        total = base_val * multiplier

        # Add half value of the unit if 'ခွဲ' was present
        if has_half:
            total += multiplier / 2

        return str(int(total))

    # Fallback lookup for single-word amounts
    if text in BURMESE_WORDS:
        return str(BURMESE_WORDS[text])

    # Final attempt: extract any leading standard digits
    cleaned = normalize_burmese_digits(text)
    match = re.search(r'\d+', cleaned)
    if match:
        return match.group(0)

    return raw