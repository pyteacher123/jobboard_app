import pytest
from core.business_logic.dto import AddCompanyDTO
from core.business_logic.exceptions import CompanyAlreadyExists, CompanyNotExists
from core.business_logic.services import create_company, get_companies, get_company_by_id
from core.models import Company
from django.core.files.uploadedfile import InMemoryUploadedFile


@pytest.mark.django_db
def test_create_company_successfully(png_for_test: InMemoryUploadedFile) -> None:
    data = AddCompanyDTO(name="EPAM", employees_number=100000, logo=png_for_test)
    company_id = create_company(data=data)
    assert type(company_id) == int

    company_from_db = Company.objects.get(pk=company_id)
    assert company_from_db.name == "EPAM"
    assert company_from_db.employees_number == 100000


@pytest.mark.django_db
def test_create_company_by_duplicate_name(png_for_test: InMemoryUploadedFile) -> None:
    data = AddCompanyDTO(name="Uber", employees_number=100000, logo=png_for_test)
    with pytest.raises(CompanyAlreadyExists):
        create_company(data=data)


@pytest.mark.django_db
def test_get_all_companies_successfully() -> None:
    result = get_companies()
    companies_names = [row.name for row in result]

    # TODO: add test case to check order!

    assert len(result) == 2
    assert "Uber" in companies_names
    assert "Google" in companies_names


@pytest.mark.django_db
def test_get_company_by_id_successfully() -> None:
    company = Company.objects.get(name="Uber")
    company_id = company.id
    result = get_company_by_id(company_id=company_id)

    assert result.id == company_id
    assert result.name == "Uber"


@pytest.mark.django_db
def test_get_company_by_invalid_id() -> None:
    company_id = 1082941942
    with pytest.raises(CompanyNotExists):
        get_company_by_id(company_id=company_id)

    with pytest.raises(Company.DoesNotExist):
        Company.objects.get(pk=company_id)
