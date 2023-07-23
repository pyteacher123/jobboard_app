from dataclasses import dataclass

from django.core.files.uploadedfile import InMemoryUploadedFile


@dataclass
class AddCompanyDTO:
    name: str
    employees_number: int
    logo: InMemoryUploadedFile
