"""
Module with business logic and data storages implementations.
"""
from dataclasses import dataclass


@dataclass
class Vacancy:
    name: str
    company: str
    level: str
    expirience: str
    min_salary: int | None
    max_salary: int | None
    id: int | None = None


@dataclass
class Company:
    name: str
    employees_number: int
    vacancies_counter: int = 0
    id: int | None = None


class CompanyDuplicateNameError(Exception):
    ...


class CompanyNotExistsError(Exception):
    ...


class CompanyStorage:
    ID_COUNT = 0

    def __init__(self) -> None:
        self._companies: list[Company] = []

    def _validate_company(self, company_to_add: Company) -> None:
        for company in self._companies:
            if company.name.lower() == company_to_add.name.lower():
                raise CompanyDuplicateNameError

    def add_company(self, company_to_add: Company) -> None:
        self._validate_company(company_to_add=company_to_add)
        self.ID_COUNT += 1
        company_to_add.id = self.ID_COUNT
        self._companies.append(company_to_add)

    def get_all_companies(self) -> list[Company]:
        return self._companies

    def get_company_by_name(self, company_name: str) -> Company | None:
        for company in self._companies:
            if company.name.lower() == company_name.lower():
                return company
        return None


class VacancyStorage:
    ID_COUNT = 0

    def __init__(self, company_storage: CompanyStorage) -> None:
        self._vacancies: list[Vacancy] = []
        self._company_storage = company_storage

    def add_vacancy(self, vacancy_to_add: Vacancy) -> None:
        company = self._company_storage.get_company_by_name(company_name=vacancy_to_add.company)
        if not company:
            raise CompanyNotExistsError

        self.ID_COUNT += 1
        vacancy_to_add.id = self.ID_COUNT
        self._vacancies.append(vacancy_to_add)
        company.vacancies_counter += 1

    def get_all_vacancies(self) -> list[Vacancy]:
        return self._vacancies
