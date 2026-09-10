import re


def mask_pii(text: str) -> str:
    """Mask common PII patterns before logging/printing."""
    # Aadhaar: 12 digits, often in groups of 4 (e.g., 1234 5678 9012)
    text = re.sub(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', 'XXXX-XXXX-XXXX', text)

    # PAN: 5 letters + 4 digits + 1 letter (e.g., ABCDE1234F)
    text = re.sub(r'\b[A-Z]{5}\d{4}[A-Z]\b', 'XXXXX0000X', text)

    # Card numbers: 13-19 digits, possibly with spaces/dashes
    text = re.sub(r'\b\d{13,19}\b', lambda m: 'X' * (len(m.group()) - 4) + m.group()[-4:], text)

    return text


if __name__ == "__main__":
    test_cases = [
        "My Aadhaar number is 1234 5678 9012",
        "My PAN is ABCDE1234F",
        "My card number is 4111111111111111",
        "My account balance is Rs. 42500.50",  # should NOT be masked
    ]
    for t in test_cases:
        print(f"Original: {t}")
        print(f"Masked:   {mask_pii(t)}")
        print("---")