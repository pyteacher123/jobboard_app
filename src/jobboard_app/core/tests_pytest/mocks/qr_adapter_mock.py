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


class QRApiAdapterMock:
    def get_qr(self, data: str) -> InMemoryUploadedFile:
        return get_test_file()
