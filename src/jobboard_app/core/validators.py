from django.core.exceptions import ValidationError


def validate_swear_words_in_company_name(value: str) -> None:
    if "fuck" in value.lower():
        raise ValidationError(message="Company name contains swear word.")
    else:
        return None


class ValidateMaxTagCount:
    def __init__(self, max_count: int) -> None:
        self._max_count = max_count

    def __call__(self, value: str) -> None:
        number_of_tags = len(value.split("\r\n"))

        if number_of_tags > self._max_count:
            raise ValidationError(message=f"Max number of tags is {self._max_count}")
        else:
            return None
