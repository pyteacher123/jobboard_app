from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.decorators import api_view
from rest_framework.response import Response

if TYPE_CHECKING:
    from rest_framework.request import Request

from core.business_logic.dto import AddCompanyDTO
from core.business_logic.services import create_company, get_companies, get_company_by_id
from core.presentation.api_v1.serializers import CompanyInfoSerializer, CompanySerializer, CreateCompanySerializer
from core.presentation.common.converters import convert_data_from_form_to_dto


@api_view(http_method_names=["GET", "POST"])
def companies_api_controller(request: Request) -> Response:
    if request.method == "GET":
        companies = get_companies()
        companies_serializer = CompanyInfoSerializer(companies, many=True)
        return Response(data=companies_serializer.data)
    else:
        serializer = CreateCompanySerializer(data=request.data)
        if serializer.is_valid():
            data = convert_data_from_form_to_dto(dto=AddCompanyDTO, data_from_form=serializer.validated_data)
            company_id = create_company(data=data)

        data = {"message": "Company created successfully", "company_id": company_id}
        return Response(data=data)


@api_view(http_method_names=["GET"])
def get_company_api_controller(request: Request, company_id: int) -> Response:
    company = get_company_by_id(company_id=company_id)
    company_serializer = CompanySerializer(company)
    return Response(data=company_serializer.data)
