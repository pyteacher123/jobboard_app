from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.decorators import permission_required
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers
from rest_framework.decorators import api_view, parser_classes, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

if TYPE_CHECKING:
    from rest_framework.request import Request

from core.business_logic.dto import AddCompanyDTO
from core.business_logic.services import create_company, get_companies, get_company_by_id
from core.presentation.api_v1.serializers import (
    CompanyInfoSerializer,
    CompanySerializer,
    CreateCompanyResponseSerializer,
    CreateCompanySerializer,
)
from core.presentation.common.converters import convert_data_from_form_to_dto


@swagger_auto_schema(
    method="POST",
    manual_parameters=[
        openapi.Parameter(name="name", description="Copmany name", in_=openapi.IN_FORM, type=openapi.TYPE_STRING),
        openapi.Parameter(name="employees_number", in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER),
        openapi.Parameter(name="logo", in_=openapi.IN_FORM, type=openapi.TYPE_FILE),
    ],
    responses={200: openapi.Response(description="Successfull response", schema=CreateCompanyResponseSerializer)},
)
@api_view(http_method_names=["GET", "POST"])
@parser_classes([parsers.MultiPartParser])
@permission_required(["core.add_company"])
@permission_classes([IsAuthenticated])
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
        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

        data = {"message": "Company created successfully", "company_id": company_id}
        return Response(data=data)


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def get_company_api_controller(request: Request, company_id: int) -> Response:
    company = get_company_by_id(company_id=company_id)
    company_serializer = CompanySerializer(company)
    return Response(data=company_serializer.data)
