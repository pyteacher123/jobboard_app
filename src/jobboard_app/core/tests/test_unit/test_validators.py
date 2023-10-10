from unittest import TestCase

from core.presentation.common.validators import FileExtensionValidator, FileSizeValidator, MaxTagCountValidator
from core.tests.mocks import FileMock


class ValidatorsTests(TestCase):
    def test_validate_file_size_succefully(self) -> None:
        validator = FileSizeValidator(max_size=10_000_000)
        test_file = FileMock(size=5_000_000)

        result = validator(value=test_file)

        self.assertEqual(result, {"status": True})

    def test_validate_file_size_validation_failed(self) -> None:
        validator = FileSizeValidator(max_size=10_000_000)
        test_file = FileMock(size=15_000_000)

        result = validator(value=test_file)

        self.assertEqual(result, {"status": False, "message": "Max file size is 10 MB"})

    def test_validate_file_extension_successfully(self) -> None:
        validator = FileExtensionValidator(available_extensions=["pdf"])
        test_file = FileMock(name="test.pdf")

        result = validator(value=test_file)

        self.assertEqual(result, {"status": True})

    def test_validate_file_extension_invalid_file_name(self) -> None:
        validator = FileExtensionValidator(available_extensions=["pdf"])
        test_file = FileMock(name="test")

        result = validator(value=test_file)

        self.assertEqual(result, {"status": False, "message": "Accept only ['pdf']"})

    def test_validate_file_extension_invalid_file_extension(self) -> None:
        validator = FileExtensionValidator(available_extensions=["pdf"])
        test_file = FileMock(name="test.png")

        result = validator(value=test_file)

        self.assertEqual(result, {"status": False, "message": "Accept only ['pdf']"})

    def test_validate_max_tag_count_successfully(self) -> None:
        validator = MaxTagCountValidator(max_count=3)
        tags = "Python\r\nPostgres"

        result = validator(value=tags)

        self.assertEqual(result, {"status": True})

    def test_validate_max_tag_count_validation_failed(self) -> None:
        validator = MaxTagCountValidator(max_count=3)
        tags = "Python\r\nPostgres\r\nHttp\r\nDocker"

        result = validator(value=tags)

        self.assertEqual(result, {"status": False, "message": "Max number of tags is 3"})
