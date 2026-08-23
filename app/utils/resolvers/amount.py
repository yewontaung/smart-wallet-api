import re
from typing import Optional, Union

# Burmese digit translation map
BURMESE_DIGITS = {
    '၀': '0', '၁': '1', '၂': '2', '၃': '3', '၄': '4',
    '၅': '5', '၆': '6', '၇': '7', '၈': '8', '၉': '9'
}

# Burmese word-to-number mapping for units
BURMESE_WORDS = {
    'တစ်': 1, 'တ': 1, '၁': 1,
    'နှစ်': 2, '၂': 2,
    'သုံး': 3, '၃': 3,
    'လေး': 4, '၄': 4,
    'ငါး': 5, '၅': 5,
    'ခြောက်': 6, '၆': 6,
    'ခုနှစ်': 7, 'ခွန်': 7, '၇': 7,
    'ရှစ်': 8, '၈': 8,
    'ကိုး': 9, '၉': 9,
    'ဆယ်': 10, '၁၀': 10
}

# Unit multipliers
BURMESE_UNITS = {
    'ရာ': 100,
    'ထောင်': 1000,
    'သောင်း': 10000,
    'သိန်း': 100000,
    'သန်း': 1000000,
    'ကုဋေ': 10000000
}


def normalize_burmese_digits(text: str) -> str:
    """Converts Burmese numerical digits (၀-၉) to English ASCII digits (0-9)."""
    return "".join(BURMESE_DIGITS.get(char, char) for char in text)


def resolve_burmese_amount(val: Optional[Union[str, int, float]]) -> Optional[str]:
    """
    Parses Burmese currency and numerical amounts into standard ASCII integer strings.
    Handles digits, words, multipliers, and half-unit fractions ('ခွဲ').
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

    # Clean text input (remove spaces and common suffixes like 'ကျပ်')
    text = raw.replace(" ", "").replace("ကျပ်", "")

    # Check for half-unit modifier 'ခွဲ' (e.g., ၅သောင်းခွဲ = 50,000 + 5,000 = 55,000)
    has_half = 'ခွဲ' in text
    if has_half:
        text = text.replace('ခွဲ', '')

    base_val = 0
    multiplier = 1
    matched_unit = None

    # Detect unit multiplier
    for unit_name, unit_val in BURMESE_UNITS.items():
        if unit_name in text:
            matched_unit = unit_name
            multiplier = unit_val
            break

    if matched_unit:
        prefix = text.split(matched_unit)[0].strip()

        # Extract numerical prefix (e.g., 'ငါး' in 'ငါးထောင်' or '၅' in '၅သောင်း')
        if not prefix:
            base_val = 1  # Default to 1 if unit stands alone like 'သိန်း'
        elif prefix in BURMESE_WORDS:
            base_val = BURMESE_WORDS[prefix]
        else:
            # Try converting Burmese digits from the prefix
            clean_prefix = normalize_burmese_digits(prefix)
            try:
                base_val = float(clean_prefix)
            except ValueError:
                base_val = 1

        total = base_val * multiplier

        # Add half value of the unit if 'ခွဲ' was present
        if has_half:
            total += multiplier / 2

        return str(int(total))

    # Fallback lookup for single-word amounts (e.g., 'ငါးထောင်')
    if text in BURMESE_WORDS:
        return str(BURMESE_WORDS[text])

    # Final attempt: extract any leading standard digits
    cleaned = normalize_burmese_digits(text)
    match = re.search(r'\d+', cleaned)
    if match:
        return match.group(0)

    return raw