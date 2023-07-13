from __future__ import annotations

from typing import TYPE_CHECKING

from dacite import from_dict
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest

from core.dto import AddCompanyDTO, AddVacancyDTO, SearchVacancyDTO
from core.exceptions import CompanyNotExists
from core.forms import AddCompanyForm, AddVacancyForm, SearchVacancyForm
from core.services import (
    create_company,
    create_vacancy,
    get_companies,
    get_company_by_id,
    get_vacancy_by_id,
    search_vacancies,
)


@require_http_methods(request_method_list=["GET"])
def index_controller(request: HttpRequest) -> HttpResponse:
    filters_form = SearchVacancyForm(request.GET)
    if filters_form.is_valid():
        search_filters = from_dict(SearchVacancyDTO, filters_form.cleaned_data)

        vacancies = search_vacancies(search_filters=search_filters)

        form = SearchVacancyForm()
        context = {"vacancies": vacancies, "form": form}
        return render(request=request, template_name="index.html", context=context)
    else:
        context = {"form": filters_form}
        return render(request=request, template_name="index.html", context=context)


@require_http_methods(request_method_list=["GET", "POST"])
def add_company_controller(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = AddCompanyForm()
        context = {"form": form}
        return render(request=request, template_name="add_company.html", context=context)

    elif request.method == "POST":
        form = AddCompanyForm(data=request.POST)
        if form.is_valid():
            data = from_dict(AddCompanyDTO, form.cleaned_data)
            create_company(data=data)

        return HttpResponseRedirect(redirect_to=reverse("company-list"))


@require_http_methods(request_method_list=["GET"])
def company_list_controller(request: HttpRequest) -> HttpResponse:
    companies = get_companies()
    context = {"companies": companies}
    return render(request=request, template_name="company_list.html", context=context)


@transaction.non_atomic_requests
@require_http_methods(request_method_list=["GET", "POST"])
def add_vacancy_controller(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = AddVacancyForm()
        context = {"form": form}
        return render(request=request, template_name="add_vacancy.html", context=context)

    elif request.method == "POST":
        form = AddVacancyForm(data=request.POST)
        if form.is_valid():
            data = from_dict(AddVacancyDTO, form.cleaned_data)
            try:
                create_vacancy(data=data)
            except CompanyNotExists:
                return HttpResponseBadRequest(content="Provided company doesn't exist.")
        else:
            context = {"form": form}
            return render(request=request, template_name="add_vacancy.html", context=context)

        return HttpResponseRedirect(redirect_to=reverse("index"))


@require_http_methods(request_method_list=["GET"])
def get_vacancy_controller(request: HttpRequest, vacancy_id: int) -> HttpResponse:
    vacancy, tags = get_vacancy_by_id(vacancy_id=vacancy_id)
    context = {"vacancy": vacancy, "tags": tags}
    return render(request=request, template_name="get_vacancy.html", context=context)


@require_http_methods(request_method_list=["GET"])
def get_company_controller(request: HttpRequest, company_id: int) -> HttpResponse:
    company = get_company_by_id(company_id=company_id)
    context = {"company": company}
    return render(request=request, template_name="get_company.html", context=context)
