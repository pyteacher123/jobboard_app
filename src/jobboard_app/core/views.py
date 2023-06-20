from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse
from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpRequest

from .services import CompanyStorage, VacancyStorage

company_storage = CompanyStorage()
vacancy_storage = VacancyStorage(company_storage=company_storage)


def index_controller(request: HttpRequest) -> HttpResponse:
    vacancies = vacancy_storage.get_all_vacancies()
    print(vacancies)
    res = render(request=request, template_name="index.html")
    return res
