from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from django.db.models import Count
from django.db.utils import IntegrityError

if TYPE_CHECKING:
    from core.business_logic.dto import AddCompanyDTO

from core.business_logic.exceptions import CompanyAlreadyExists, CompanyNotExists
from core.business_logic.services.common import change_file_size, replace_file_name_to_uuid
from core.models import Company

logger = logging.getLogger(__name__)


def create_company(data: AddCompanyDTO) -> Any:
    data.logo = replace_file_name_to_uuid(file=data.logo)
    data.logo = change_file_size(file=data.logo)
    try:
        company = Company.objects.create(name=data.name, employees_number=data.employees_number, logo=data.logo)
    except IntegrityError:
        raise CompanyAlreadyExists
    logger.info(f"Created file with filename {data.logo.name}")
    return company.id


def get_companies() -> list[Company]:
    companies = Company.objects.annotate(vacancy__count=Count("vacancy__id")).order_by("-vacancy__count")
    return list(companies)


def get_company_by_id(company_id: int) -> Company:
    try:
        company: Company = Company.objects.annotate(vacancy__count=Count("vacancy__id")).get(pk=company_id)
    except Company.DoesNotExist:
        raise CompanyNotExists
    logger.info("Succefully got company.", extra={"company_id": str(company.id), "company_name": company.name})
    return company
