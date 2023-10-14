import io

import pytest
from core.models import Company
from dirty_equals import IsListOrTuple, IsPositiveInt, IsStr
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_get_companies_successfully(api_client: APIClient) -> None:
    response = api_client.get("/api/v1/companies/")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == IsListOrTuple(
        {"id": IsPositiveInt, "name": IsStr, "employees_number": IsPositiveInt, "vacancy__count": IsPositiveInt},
        length=...,
    )
    assert len(response_data) == 2


@pytest.mark.django_db
def test_get_company_by_id_successfully(api_client: APIClient) -> None:
    # api_client.login(username="max", password="123456")  # noqa
    company = Company.objects.get(name="Uber")
    company_id = company.id
    response = api_client.get(f"/api/v1/companies/{company_id}/")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        "id": IsPositiveInt,
        "name": IsStr,
        "employees_number": IsPositiveInt,
        "vacancy__count": IsPositiveInt,
        "logo": IsStr,
    }
    assert response_data["name"] == "Uber"


@pytest.mark.django_db
def test_get_company_by_invalid_id(api_client: APIClient) -> None:
    # api_client.login(username="max", password="123456")  # noqa
    company_id = 12411
    response = api_client.get(f"/api/v1/companies/{company_id}/")
    response_data = response.json()

    assert response.status_code == 404
    assert response_data["message"] == "Company with provided id doesn't exist."


@pytest.mark.django_db
def test_create_company_successfully(api_client: APIClient, png_bytes: io.BytesIO) -> None:
    png_bytes.name = "test.png"
    data = {
        "name": "Test Company",
        "employees_number": "1000",
        "logo": png_bytes,  # TODO: check how to send file via APIClient.
    }

    response = api_client.post(path="/api/v1/companies/", data=data)
    response_data = response.json()

    assert response == 200
    assert response_data == {"message": "Company created successfully", "company_id": IsPositiveInt}
