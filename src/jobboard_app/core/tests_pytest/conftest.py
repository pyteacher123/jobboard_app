import pytest
from core.models import Company, Level, Tag, Vacancy
from core.tests.mocks import QRApiAdapterMock
from core.tests_pytest.utils import get_test_file, get_test_pdf
from django.core.files.uploadedfile import InMemoryUploadedFile


@pytest.fixture
def pdf_for_test() -> InMemoryUploadedFile:
    return get_test_pdf()


@pytest.fixture
def png_for_test() -> InMemoryUploadedFile:
    return get_test_file()


@pytest.fixture(autouse=True)
def populate_db(png_for_test: InMemoryUploadedFile, pdf_for_test: InMemoryUploadedFile) -> None:
    company1 = Company.objects.create(name="Uber", employees_number=1000, logo=png_for_test)
    company2 = Company.objects.create(name="Google", employees_number=1000, logo=png_for_test)
    level1 = Level.objects.get(name="Junior")
    tag1 = Tag.objects.create(name="Python")
    tag2 = Tag.objects.create(name="Airflow")

    vacancy1 = Vacancy.objects.create(
        name="Python Developer",
        level=level1,
        company=company1,
        expirience="0 years",
        min_salary=1000,
        max_salary=5000,
        attachment=pdf_for_test,
    )
    vacancy1.tags.set([tag1])

    vacancy2 = Vacancy.objects.create(
        name="Data Engineer",
        level=level1,
        company=company2,
        expirience="0 years",
        min_salary=1000,
        max_salary=2000,
        attachment=pdf_for_test,
    )
    vacancy2.tags.set([tag1, tag2])


@pytest.fixture
def qr_adapter_mock() -> QRApiAdapterMock:
    return QRApiAdapterMock()
