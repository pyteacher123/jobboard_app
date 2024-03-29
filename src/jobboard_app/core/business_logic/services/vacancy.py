from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.conf import settings
from django.db import transaction
from django.db.models import QuerySet

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser

    from core.business_logic.dto import SearchVacancyDTO, AddVacancyDTO, ApplyVacancyDTO
    from core.business_logic.interfaces import QRApiAdaptarProtocol

from core.business_logic.exceptions import CompanyNotExists, VacancyNotExists
from core.business_logic.services.common import replace_file_name_to_uuid
from core.models import Company, JobResponse, Level, Tag, Vacancy

logger = logging.getLogger(__name__)


def search_vacancies(search_filters: SearchVacancyDTO) -> QuerySet[Vacancy]:
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

    vacancies = vacancies.order_by("-id")

    return vacancies


def create_vacancy(data: AddVacancyDTO, qr_adapter: QRApiAdaptarProtocol) -> None:
    with transaction.atomic():
        tags: list[str] = data.tags.split("\r\n")
        tags_list: list[Tag] = []
        for tag in tags:
            tag = tag.lower()
            try:
                tag_from_db = Tag.objects.get(name=tag)
            except Tag.DoesNotExist:
                logger.warning("Tag doesn't exists", extra={"tag": tag})
                tag_from_db = Tag.objects.create(name=tag)
                logger.info("Handled error and successfully created tag in db.", extra={"tag": tag})

            tags_list.append(tag_from_db)

        level = Level.objects.get(name=data.level)
        try:
            company = Company.objects.get(name=data.company_name)
        except Company.DoesNotExist:
            logger.error("Company doesn't exists.", extra={"company": data.company_name})
            raise CompanyNotExists

        data.attachment = replace_file_name_to_uuid(file=data.attachment)

        created_vacancy = Vacancy.objects.create(
            name=data.name,
            level=level,
            company=company,
            expirience=data.expirience,
            min_salary=data.min_salary,
            max_salary=data.max_salary,
            attachment=data.attachment,
        )

        created_vacancy.tags.set(tags_list)

        data = f"{settings.SERVER_HOST}/vacancy/{created_vacancy.id}/"
        qr_code = qr_adapter.get_qr(data=data)
        created_vacancy.qr_code = qr_code
        created_vacancy.save()


def get_vacancy_by_id(vacancy_id: int) -> tuple[Vacancy, list[Tag]]:
    try:
        vacancy = Vacancy.objects.select_related("level", "company").prefetch_related("tags").get(pk=vacancy_id)
    except Vacancy.DoesNotExist:
        raise VacancyNotExists
    tags = vacancy.tags.all()
    logger.info("Got vacancy.", extra={"vacancy_id": vacancy.id})
    return vacancy, list(tags)


def apply_to_vacancy(data: ApplyVacancyDTO, vacancy_id: int, user: AbstractBaseUser) -> None:
    vacancy = Vacancy.objects.get(pk=vacancy_id)
    JobResponse.objects.create(note=data.note, cv=data.cv, vacancy=vacancy, user=user)
