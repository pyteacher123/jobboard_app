from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import connection, transaction
from django.db.models import Count
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest

from core.forms import AddCompanyForm, AddVacancyForm, SearchVacancyForm
from core.models import Company, Level, Tag, Vacancy


def print_queries() -> int:
    queries_count = 0
    for _ in connection.queries:
        queries_count += 1
    return queries_count


@require_http_methods(request_method_list=["GET"])
def index_controller(request: HttpRequest) -> HttpResponse:
    filters_form = SearchVacancyForm(request.GET)
    if filters_form.is_valid():
        vacancies = Vacancy.objects.select_related("level", "company").prefetch_related("tags")

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
            name = form.cleaned_data["name"]
            employees_number = form.cleaned_data["employees_number"]
            Company.objects.create(name=name, employees_number=employees_number)
        return HttpResponseRedirect(redirect_to=reverse("company-list"))


@require_http_methods(request_method_list=["GET"])
def company_list_controller(request: HttpRequest) -> HttpResponse:
    companies = Company.objects.annotate(vacancy__count=Count("vacancy__id")).order_by("-vacancy__count")
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
            name = form.cleaned_data["name"]
            company_name = form.cleaned_data["company_name"]
            level_name = form.cleaned_data["level"]
            expirience = form.cleaned_data["expirience"]
            min_salary = form.cleaned_data["min_salary"]
            max_salary = form.cleaned_data["max_salary"]
            tags_string: str = form.cleaned_data["tags"]

            try:
                with transaction.atomic():
                    tags: list[str] = tags_string.split("\r\n")
                    tags_list: list[Tag] = []
                    for tag in tags:
                        tag = tag.lower()
                        try:
                            tag_from_db = Tag.objects.get(name=tag)
                        except Tag.DoesNotExist:
                            tag_from_db = Tag.objects.create(name=tag)

                        tags_list.append(tag_from_db)

                    level = Level.objects.get(name=level_name)
                    company = Company.objects.get(name=company_name)

                    created_vacancy = Vacancy.objects.create(
                        name=name,
                        level=level,
                        company=company,
                        expirience=expirience,
                        min_salary=min_salary,
                        max_salary=max_salary,
                    )

                    created_vacancy.tags.set(tags_list)
            except Company.DoesNotExist:
                return HttpResponseBadRequest(content="Provided company doesn't exist.")
            finally:
                print_queries()

        else:
            context = {"form": form}
            return render(request=request, template_name="add_vacancy.html", context=context)

        return HttpResponseRedirect(redirect_to=reverse("index"))


@require_http_methods(request_method_list=["GET"])
def get_vacancy_controller(request: HttpRequest, vacancy_id: int) -> HttpResponse:
    vacancy = ...
    context = {"vacancy": vacancy}
    return render(request=request, template_name="get_vacancy.html", context=context)


@require_http_methods(request_method_list=["GET"])
def get_company_controller(request: HttpRequest, company_id: int) -> HttpResponse:
    company = ...
    context = {"company": company}
    return render(request=request, template_name="get_company.html", context=context)
