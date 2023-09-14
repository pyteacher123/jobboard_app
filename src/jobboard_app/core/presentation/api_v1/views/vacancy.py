from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.decorators import api_view
from rest_framework.response import Response

if TYPE_CHECKING:
    from rest_framework.request import Request

from core.business_logic.dto import SearchVacancyDTO
from core.business_logic.services import get_vacancy_by_id, search_vacancies
from core.presentation.api_v1.pagination import APIPaginator
from core.presentation.api_v1.serializers import SearchVacanciesSerializer, VacancyInfoSerializer, VacancySerializer
from core.presentation.common.converters import convert_data_from_form_to_dto


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


@api_view(http_method_names=["GET"])
def get_vacancy_api_controller(request: Request, vacancy_id: int) -> Response:
    vacancy, _ = get_vacancy_by_id(vacancy_id=vacancy_id)
    vacancy_serializer = VacancySerializer(vacancy)
    return Response(data=vacancy_serializer.data)
