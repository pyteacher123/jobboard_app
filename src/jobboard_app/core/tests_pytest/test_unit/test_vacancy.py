import pytest
from core.business_logic.dto import AddVacancyDTO, SearchVacancyDTO
from core.business_logic.exceptions import CompanyNotExists
from core.business_logic.services import create_vacancy, search_vacancies
from core.models import Vacancy
from core.tests_pytest.mocks import QRApiAdapterMock
from django.core.files.uploadedfile import InMemoryUploadedFile


@pytest.mark.django_db
def test_create_vacancy_successfully(pdf_for_test: InMemoryUploadedFile) -> None:
    data = AddVacancyDTO(
        name="Python Engineer",
        level="Junior",
        company_name="Uber",
        expirience="0 years",
        min_salary=None,
        max_salary=None,
        attachment=pdf_for_test,
        tags="Python\r\nPostgres",
    )

    count_before_request = Vacancy.objects.all().count()

    qr_adapter = QRApiAdapterMock()
    create_vacancy(data=data, qr_adapter=qr_adapter)

    count_after_request = Vacancy.objects.all().count()

    vacancy_from_db: Vacancy = (
        Vacancy.objects.select_related("level", "company").prefetch_related("tags").get(name=data.name)
    )
    tags_from_db = vacancy_from_db.tags.all()

    assert vacancy_from_db.name == data.name
    assert vacancy_from_db.company.name == data.company_name
    assert count_before_request + 1 == count_after_request
    expected_tags = ("python", "postgres")
    for tag in tags_from_db:
        assert tag.name in expected_tags


@pytest.mark.django_db
def test_create_vacancy_invalid_company_name(
    pdf_for_test: InMemoryUploadedFile, qr_adapter_mock: QRApiAdapterMock
) -> None:
    data = AddVacancyDTO(
        name="Python Engineer",
        level="Junior",
        company_name="Invalid Company",
        expirience="0 years",
        min_salary=None,
        max_salary=None,
        attachment=pdf_for_test,
        tags="Python\r\nPostgres",
    )

    count_before_request = Vacancy.objects.all().count()

    with pytest.raises(CompanyNotExists):
        create_vacancy(data=data, qr_adapter=qr_adapter_mock)

    count_after_request = Vacancy.objects.all().count()
    assert count_before_request == count_after_request


@pytest.mark.django_db
def test_search_vacancies_all_filters() -> None:
    data = SearchVacancyDTO(
        name="Python",
        company_name="Uber",
        level="Junior",
        expirience="0",
        min_salary=100,
        max_salary=6000,
        tag="Python",
    )
    result = search_vacancies(search_filters=data)
    vacancy = result[0]

    assert len(result) == 1
    assert "python" in vacancy.name.lower()


@pytest.mark.django_db
def test_search_vacancies_by_name() -> None:
    data = SearchVacancyDTO(
        name="er", company_name="", level="", expirience="", min_salary=None, max_salary=None, tag=""
    )
    result = search_vacancies(search_filters=data)

    assert len(result) == 2
    for vacancy in result:
        assert "er" in vacancy.name.lower()


@pytest.mark.django_db
def test_search_vacancies_by_company_name() -> None:
    data = SearchVacancyDTO(
        name="", company_name="google", level="", expirience="", min_salary=None, max_salary=None, tag=""
    )
    result = search_vacancies(search_filters=data)
    vacancy = result[0]

    assert len(result) == 1
    assert "google" in vacancy.company.name.lower()
