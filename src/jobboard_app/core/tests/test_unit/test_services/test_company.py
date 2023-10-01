from io import BytesIO
from typing import Any

from core.business_logic.dto import AddCompanyDTO
from core.business_logic.exceptions import CompanyAlreadyExists, CompanyNotExists
from core.business_logic.services import create_company, get_companies, get_company_by_id
from core.models import Company
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from PIL import Image


def get_test_file() -> InMemoryUploadedFile:
    output = BytesIO()
    image = Image.new("RGB", (100, 100))
    image.save(output, format="PNG", quality=100)
    return InMemoryUploadedFile(
        file=output, field_name=None, name="test.png", content_type="image/png", size=10, charset=None
    )


class CompanyServicesTests(TestCase):
    def setUp(self) -> Any:
        self.logo_for_test = get_test_file()
        Company.objects.create(name="Uber", employees_number=1000, logo=self.logo_for_test)
        Company.objects.create(name="Google", employees_number=1000, logo=self.logo_for_test)
        return super().setUp()

    def test_create_company_successfully(self) -> None:
        data = AddCompanyDTO(name="EPAM", employees_number=100000, logo=self.logo_for_test)
        company_id = create_company(data=data)
        self.assertIsInstance(company_id, int)

        company_from_db = Company.objects.get(pk=company_id)
        self.assertEqual(company_from_db.name, "EPAM")
        self.assertEqual(company_from_db.employees_number, 100000)

    def test_create_company_by_duplicate_name(self) -> None:
        data = AddCompanyDTO(name="Uber", employees_number=100000, logo=get_test_file())
        with self.assertRaises(CompanyAlreadyExists):
            create_company(data=data)

    def test_get_all_companies_successfully(self) -> None:
        result = get_companies()
        companies_names = [row.name for row in result]

        # TODO: add test case to check order!

        self.assertEqual(len(result), 2)
        self.assertIn("Uber", companies_names)
        self.assertIn("Google", companies_names)

    def test_get_company_by_id_successfully(self) -> None:
        company = Company.objects.get(name="Uber")
        company_id = company.id
        result = get_company_by_id(company_id=company_id)

        self.assertEqual(result.id, company_id)
        self.assertEqual(result.name, "Uber")

    def test_get_company_by_invalid_id(self) -> None:
        company_id = 1082941942
        with self.assertRaises(CompanyNotExists):
            get_company_by_id(company_id=company_id)

        with self.assertRaises(Company.DoesNotExist):
            Company.objects.get(pk=company_id)
