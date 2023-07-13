from dataclasses import dataclass


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
    tags: str


@dataclass
class AddCompanyDTO:
    name: str
    employees_number: int
