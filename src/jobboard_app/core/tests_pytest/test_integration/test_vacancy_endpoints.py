import pytest
from core.models import Vacancy
from dirty_equals import IsListOrTuple, IsPositiveInt, IsStr
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_get_all_vacancies_successfully(api_client: APIClient) -> None:
    response = api_client.get("/api/v1/vacancies/")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        "count": IsPositiveInt,
        "next": None,
        "previous": None,
        "results": IsListOrTuple(
            {
                "id": IsPositiveInt,
                "name": IsStr,
                "company": {"id": IsPositiveInt, "name": IsStr},
                "level": {"id": IsPositiveInt, "name": IsStr},
                "expirience": IsStr,
                "min_salary": IsPositiveInt,
                "max_salary": IsPositiveInt,
            },
            length=2,
        ),
    }


@pytest.mark.django_db
def test_get_all_vacancies_successfully_search_by_name(api_client: APIClient) -> None:
    response = api_client.get("/api/v1/vacancies/?name=python")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        "count": IsPositiveInt,
        "next": None,
        "previous": None,
        "results": IsListOrTuple(
            {
                "id": IsPositiveInt,
                "name": IsStr,
                "company": {"id": IsPositiveInt, "name": IsStr},
                "level": {"id": IsPositiveInt, "name": IsStr},
                "expirience": IsStr,
                "min_salary": IsPositiveInt,
                "max_salary": IsPositiveInt,
            },
            length=1,
        ),
    }
    assert response_data["results"][0]["name"] == "Python Developer"


@pytest.mark.django_db
def test_get_all_vacancies_successfully_search_by_max_salary(api_client: APIClient) -> None:
    response = api_client.get("/api/v1/vacancies/?max_salary=4000")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        "count": IsPositiveInt,
        "next": None,
        "previous": None,
        "results": IsListOrTuple(
            {
                "id": IsPositiveInt,
                "name": IsStr,
                "company": {"id": IsPositiveInt, "name": IsStr},
                "level": {"id": IsPositiveInt, "name": IsStr},
                "expirience": IsStr,
                "min_salary": IsPositiveInt,
                "max_salary": IsPositiveInt,
            },
            length=1,
        ),
    }
    assert response_data["results"][0]["name"] == "Data Engineer"
    assert response_data["results"][0]["max_salary"] <= 4000


@pytest.mark.django_db
def test_get_vacancy_by_id_successfully(api_client: APIClient) -> None:
    vacancy = Vacancy.objects.get(name="Python Developer")
    vacancy_id = vacancy.id

    response = api_client.get(f"/api/v1/vacancies/{vacancy_id}/")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        "id": IsPositiveInt,
        "name": IsStr,
        "company": {"id": IsPositiveInt, "name": IsStr},
        "level": {"id": IsPositiveInt, "name": IsStr},
        "expirience": IsStr,
        "min_salary": IsPositiveInt,
        "max_salary": IsPositiveInt,
        "tags": IsListOrTuple({"id": IsPositiveInt, "name": IsStr}, length=...),
    }
    assert response_data["name"] == "Python Developer"


@pytest.mark.django_db
def test_get_vacancy_by_invalid_id(api_client: APIClient) -> None:
    vacancy_id = 1248324234
    response = api_client.get(f"/api/v1/vacancies/{vacancy_id}/")
    response_data = response.json()

    assert response.status_code == 404
    assert response_data["message"] == "Vacancy with provided id doesn't exist."
