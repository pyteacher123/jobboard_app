from django.core.exceptions import ValidationError


def validate_swear_words_in_company_name(value: str) -> None:
    if "fuck" in value.lower():
        raise ValidationError(message="Company name contains swear word.")
    else:
        return None
