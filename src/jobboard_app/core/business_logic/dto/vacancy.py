from dataclasses import dataclass

from django.core.files import File


@dataclass
class SearchVacancyDTO:
    name: str
    company_name: str
    level: str
    expirience: str
    min_salary: int | None
    max_salary: int | None
    tag: str


@dataclass
class AddVacancyDTO:
    name: str
    level: str
    company_name: str
    expirience: str
    min_salary: int | None
    max_salary: int | None
    attachment: File
    tags: str
