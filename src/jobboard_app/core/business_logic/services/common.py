from __future__ import annotations

import sys
import uuid
from io import BytesIO
from typing import TYPE_CHECKING

import requests
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

if TYPE_CHECKING:
    from django.core.files import File

from core.business_logic.exceptions import QRCodeServiceUnavailable


def replace_file_name_to_uuid(file: File) -> File:
    file_extansion = file.name.split(".")[-1]
    file_name = str(uuid.uuid4())
    file.name = file_name + "." + file_extansion
    return file


def change_file_size(file: InMemoryUploadedFile) -> InMemoryUploadedFile:
    format = file.content_type.split("/")[-1].upper()
    output = BytesIO()
    with Image.open(file) as image:
        image.thumbnail(size=(200, 150))
        image.save(output, format=format, quality=100)

    return InMemoryUploadedFile(
        file=output,
        field_name=file.field_name,
        name=file.name,
        content_type=file.content_type,
        size=sys.getsizeof(output),
        charset=file.charset,
    )


def get_qr_code(data: str) -> InMemoryUploadedFile:
    response = requests.get(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={data}")
    if response.status_code == 200:
        output = BytesIO(response.content)
        return InMemoryUploadedFile(
            file=output,
            field_name=None,
            name=str(uuid.uuid4()) + ".png",
            content_type="image/png",
            size=sys.getsizeof(output),
            charset=None,
        )
    else:
        raise QRCodeServiceUnavailable
