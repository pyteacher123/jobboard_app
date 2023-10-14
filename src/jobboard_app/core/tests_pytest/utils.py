import sys
import tempfile
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


def get_test_file() -> InMemoryUploadedFile:
    output = BytesIO()
    image = Image.new("RGB", (100, 100))
    image.save(output, format="PNG", quality=100)
    return InMemoryUploadedFile(
        file=output, field_name=None, name="test.png", content_type="image/png", size=10, charset=None
    )


def get_test_file_bytes() -> BytesIO:
    output = BytesIO()
    image = Image.new("RGB", (100, 100))
    image.save(output, format="PNG", quality=100)
    return output


def get_test_pdf() -> InMemoryUploadedFile:
    with tempfile.NamedTemporaryFile(mode="w+b", suffix=".pdf") as file:
        output = BytesIO(file.read())
        return InMemoryUploadedFile(
            file=output,
            field_name=None,
            name="test.pdf",
            content_type="application/pdf",
            size=sys.getsizeof(file),
            charset=None,
        )
