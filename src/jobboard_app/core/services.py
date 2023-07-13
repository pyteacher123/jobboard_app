from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import transaction
from django.db.models import Count

if TYPE_CHECKING:
    from core.dto import SearchVacancyDTO, AddVacancyDTO, AddCompanyDTO

from core.exceptions import CompanyNotExists
from core.models import Company, Level, Tag, Vacancy


def search_vacancies(search_filters: SearchVacancyDTO) -> list[Vacancy]:
    vacancies = Vacancy.objects.select_related("level", "company").prefetch_related("tags")

    if search_filters.name:
        vacancies = vacancies.filter(name__icontains=search_filters.name)

    if search_filters.company_name:
        vacancies = vacancies.filter(company__name__icontains=search_filters.company_name)

    if search_filters.level:
        vacancies = vacancies.filter(level__name=search_filters.level)

    if search_filters.expirience:
        vacancies = vacancies.filter(expirience__icontains=search_filters.expirience)

    if search_filters.min_salary:
        vacancies = vacancies.filter(min_salary__gte=search_filters.min_salary)

    if search_filters.max_salary:
        vacancies = vacancies.filter(max_salary__lte=search_filters.max_salary)

    if search_filters.tag:
        vacancies = vacancies.filter(tags__name=search_filters.tag)

    return list(vacancies)


def create_company(data: AddCompanyDTO) -> None:
    Company.objects.create(name=data.name, employees_number=data.employees_number)


def get_companies() -> list[Company]:
    companies = Company.objects.annotate(vacancy__count=Count("vacancy__id")).order_by("-vacancy__count")
    return list(companies)


def create_vacancy(data: AddVacancyDTO) -> None:
    with transaction.atomic():
        tags: list[str] = data.tags.split("\r\n")
        tags_list: list[Tag] = []
        for tag in tags:
            tag = tag.lower()
            try:
                tag_from_db = Tag.objects.get(name=tag)
            except Tag.DoesNotExist:
                tag_from_db = Tag.objects.create(name=tag)

            tags_list.append(tag_from_db)

        level = Level.objects.get(name=data.level)
        try:
            company = Company.objects.get(name=data.company_name)
        except Company.DoesNotExist:
            raise CompanyNotExists

        created_vacancy = Vacancy.objects.create(
            name=data.name,
            level=level,
            company=company,
            expirience=data.expirience,
            min_salary=data.min_salary,
            max_salary=data.max_salary,
        )

        created_vacancy.tags.set(tags_list)


def get_vacancy_by_id(vacancy_id: int) -> tuple[Vacancy, list[Tag]]:
    vacancy = Vacancy.objects.select_related("level", "company").prefetch_related("tags").get(pk=vacancy_id)
    tags = vacancy.tags.all()
    return vacancy, list(tags)


def get_company_by_id(company_id: int) -> Company:
    company: Company = Company.objects.annotate(vacancy__count=Count("vacancy__id")).get(pk=company_id)
    return company
