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


class BaseStorage:
    ID_COUNT = 0

    def update_counter(self) -> int:
        self.ID_COUNT += 1
        return self.ID_COUNT


class CompanyStorage(BaseStorage):
    def __init__(self) -> None:
        self._companies: list[Company] = []

    def _validate_company(self, company_to_add: Company) -> None:
        for company in self._companies:
            if company.name.lower() == company_to_add.name.lower():
                raise CompanyDuplicateNameError

    def add_company(self, company_to_add: Company) -> None:
        self._validate_company(company_to_add=company_to_add)
        primary_key = self.update_counter()
        company_to_add.id = primary_key
        self._companies.append(company_to_add)

    def get_all_companies(self) -> list[Company]:
        return self._companies

    def get_company_by_name(self, company_name: str) -> Company | None:
        for company in self._companies:
            if company.name.lower() == company_name.lower():
                return company
        return None

    def get_company_by_id(self, company_id: int) -> Company | None:
        for company in self._companies:
            if company.id == company_id:
                return company
        return None


class VacancyStorage(BaseStorage):
    def __init__(self, company_storage: CompanyStorage) -> None:
        self._vacancies: list[Vacancy] = []
        self._company_storage = company_storage

    def add_vacancy(self, vacancy_to_add: Vacancy) -> None:
        company = self._company_storage.get_company_by_name(company_name=vacancy_to_add.company)
        if not company:
            raise CompanyNotExistsError

        primary_key = self.update_counter()
        vacancy_to_add.id = primary_key
        self._vacancies.append(vacancy_to_add)
        company.vacancies_counter += 1

    def get_all_vacancies(self) -> list[Vacancy]:
        return self._vacancies

    def get_vacancy_by_id(self, vacancy_id: int) -> Vacancy | None:
        for vacancy in self._vacancies:
            if vacancy.id == vacancy_id:
                return vacancy
        return None
