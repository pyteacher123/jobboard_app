from __future__ import annotations

from typing import TYPE_CHECKING

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers
from rest_framework.decorators import api_view, parser_classes, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

if TYPE_CHECKING:
    from rest_framework.request import Request

from core.business_logic.dto import AddCompanyDTO
from core.business_logic.exceptions import CompanyNotExists
from core.business_logic.services import create_company, get_companies, get_company_by_id
from core.presentation.api_v1.serializers import (
    CompanyInfoSerializer,
    CompanySerializer,
    CreateCompanyResponseSerializer,
    CreateCompanySerializer,
    ErrorSerializer,
)
from core.presentation.common.converters import convert_data_from_form_to_dto


@swagger_auto_schema(
    method="POST",
    manual_parameters=[
        openapi.Parameter(name="name", description="Copmany name", in_=openapi.IN_FORM, type=openapi.TYPE_STRING),
        openapi.Parameter(name="employees_number", in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER),
        openapi.Parameter(name="logo", in_=openapi.IN_FORM, type=openapi.TYPE_FILE),
    ],
    responses={
        200: openapi.Response(description="Successfull response", schema=CreateCompanyResponseSerializer),
        400: openapi.Response(description="Provided invalid data"),
        500: openapi.Response(description="Unhandled server error"),
    },
)
@swagger_auto_schema(
    method="GET",
    responses={
        200: openapi.Response(description="Successfull response", schema=CompanyInfoSerializer(many=True)),
        500: openapi.Response(description="Unhandled server error"),
    },
)
@api_view(http_method_names=["GET", "POST"])
@parser_classes([parsers.MultiPartParser])
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


@swagger_auto_schema(
    method="GET",
    manual_parameters=[openapi.Parameter(name="company_id", in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER)],
    responses={
        200: openapi.Response(description="Successfull response", schema=CompanySerializer),
        500: openapi.Response(description="Unhandled server error"),
        404: openapi.Response(description="Resource not found", schema=ErrorSerializer),
    },
)
@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def get_company_api_controller(request: Request, company_id: int) -> Response:
    try:
        company = get_company_by_id(company_id=company_id)
    except CompanyNotExists:
        data = {"message": "Company with provided id doesn't exist."}
        return Response(data=data, status=HTTP_404_NOT_FOUND)
    company_serializer = CompanySerializer(company)
    return Response(data=company_serializer.data)
