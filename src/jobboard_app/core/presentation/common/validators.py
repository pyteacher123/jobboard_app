from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import NotRequired, TypedDict

if TYPE_CHECKING:
    from django.core.files import File


class ValidatorResponse(TypedDict):
    status: bool
    message: NotRequired[str]


class FileExtensionValidator:
    def __init__(self, available_extensions: list[str]) -> None:
        self._available_extensions = available_extensions

    def __call__(self, value: File) -> ValidatorResponse:
        split_file_name = value.name.split(".")
        if len(split_file_name) < 2:
            return {"status": False, "message": f"Accept only {self._available_extensions}"}

        file_extension = split_file_name[-1]

        if file_extension not in self._available_extensions:
            return {"status": False, "message": f"Accept only {self._available_extensions}"}

        return {"status": True}


class FileSizeValidator:
    def __init__(self, max_size: int) -> None:
        self._max_size = max_size

    def __call__(self, value: File) -> ValidatorResponse:
        if value.size > self._max_size:
            max_size_in_mb = int(self._max_size / 1_000_000)
            return {"status": False, "message": f"Max file size is {max_size_in_mb} MB"}

        return {"status": True}


def validate_swear_words_in_company_name(value: str) -> ValidatorResponse:
    if "fuck" in value.lower():
        return {"status": False, "message": "Company name contains swear word."}

    return {"status": True}


class MaxTagCountValidator:
    def __init__(self, max_count: int) -> None:
        self._max_count = max_count

    def __call__(self, value: str) -> ValidatorResponse:
        number_of_tags = len(value.split("\r\n"))

        if number_of_tags > self._max_count:
            return {"status": False, "message": "Max number of tags is {self._max_count}"}

        return {"status": True}
