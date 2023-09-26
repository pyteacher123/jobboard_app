from __future__ import annotations

from typing import TYPE_CHECKING

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

if TYPE_CHECKING:
    from rest_framework.request import Request

from core.business_logic.dto import SearchVacancyDTO
from core.business_logic.exceptions import VacancyNotExists
from core.business_logic.services import get_vacancy_by_id, search_vacancies
from core.presentation.api_v1.pagination import APIPaginator
from core.presentation.api_v1.serializers import (
    ErrorSerializer,
    SearchVacanciesSerializer,
    VacancyInfoPaginatedResponseSerializer,
    VacancyInfoSerializer,
    VacancySerializer,
)
from core.presentation.common.converters import convert_data_from_form_to_dto


@swagger_auto_schema(
    method="GET",
    manual_parameters=[
        openapi.Parameter(name="page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter(name="name", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter(name="company_name", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter(name="level", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter(name="expirience", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter(name="min_salary", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter(name="max_salary", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter(name="tag", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ],
    responses={
        200: openapi.Response(description="Successfull response", schema=VacancyInfoPaginatedResponseSerializer),
        500: openapi.Response(description="Unhandled server error"),
    },
)
@api_view(http_method_names=["GET"])
def get_vacancies_api_controller(request: Request) -> Response:
    filters_serializer = SearchVacanciesSerializer(data=request.query_params)
    if filters_serializer.is_valid():
        data = convert_data_from_form_to_dto(dto=SearchVacancyDTO, data_from_form=filters_serializer.validated_data)
        vacancies = search_vacancies(search_filters=data)

        paginator = APIPaginator(per_page=5)
        result_page = paginator.get_queryset_paginated(queryset=vacancies, request=request)

        vacancies_info_serializer = VacancyInfoSerializer(result_page, many=True)

    return paginator.paginate(data=vacancies_info_serializer.data)


@swagger_auto_schema(
    method="GET",
    manual_parameters=[
        openapi.Parameter(name="vacancy_id", in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER),
    ],
    responses={
        200: openapi.Response(description="Successfull response", schema=VacancySerializer),
        404: openapi.Response(description="Vacancy not found", schema=ErrorSerializer),
        500: openapi.Response(description="Unhandled server error"),
    },
)
@api_view(http_method_names=["GET"])
def get_vacancy_api_controller(request: Request, vacancy_id: int) -> Response:
    try:
        vacancy, _ = get_vacancy_by_id(vacancy_id=vacancy_id)
    except VacancyNotExists:
        data = {"message": "Vacancy with provided id doesn't exist."}
        return Response(data=data, status=HTTP_404_NOT_FOUND)
    vacancy_serializer = VacancySerializer(vacancy)
    return Response(data=vacancy_serializer.data)
