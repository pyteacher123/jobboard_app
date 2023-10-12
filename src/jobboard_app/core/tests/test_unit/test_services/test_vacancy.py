import requests  # noqa
from core.business_logic.dto import AddVacancyDTO, SearchVacancyDTO
from core.business_logic.exceptions import CompanyNotExists
from core.business_logic.services import create_vacancy, search_vacancies
from core.models import Company, Level, Tag, Vacancy
from core.tests.mocks import QRApiAdapterMock
from core.tests.test_unit.utils import get_test_file, get_test_pdf
from django.test import TestCase


class VacancyServicesTests(TestCase):
    def setUp(self) -> None:
        self.logo_for_test = get_test_file()
        self.pdf_for_test = get_test_pdf()
        company1 = Company.objects.create(name="Uber", employees_number=1000, logo=self.logo_for_test)
        company2 = Company.objects.create(name="Google", employees_number=1000, logo=self.logo_for_test)
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
            attachment=self.pdf_for_test,
        )
        vacancy1.tags.set([tag1])

        vacancy2 = Vacancy.objects.create(
            name="Data Engineer",
            level=level1,
            company=company2,
            expirience="0 years",
            min_salary=1000,
            max_salary=2000,
            attachment=self.pdf_for_test,
        )
        vacancy2.tags.set([tag1, tag2])
        return super().setUp()

    def test_create_vacancy_successfully(self) -> None:
        data = AddVacancyDTO(
            name="Python Engineer",
            level="Junior",
            company_name="Uber",
            expirience="0 years",
            min_salary=None,
            max_salary=None,
            attachment=self.pdf_for_test,
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

        self.assertEqual(vacancy_from_db.name, data.name)
        self.assertEqual(vacancy_from_db.company.name, data.company_name)
        self.assertEqual(count_before_request + 1, count_after_request)
        expected_tags = ("python", "postgres")
        for tag in tags_from_db:
            self.assertIn(tag.name, expected_tags)

    def test_create_vacancy_invalid_company_name(self) -> None:
        data = AddVacancyDTO(
            name="Python Engineer",
            level="Junior",
            company_name="Invalid Company",
            expirience="0 years",
            min_salary=None,
            max_salary=None,
            attachment=self.pdf_for_test,
            tags="Python\r\nPostgres",
        )

        count_before_request = Vacancy.objects.all().count()

        with self.assertRaises(CompanyNotExists):
            qr_adapter = QRApiAdapterMock()
            create_vacancy(data=data, qr_adapter=qr_adapter)

        count_after_request = Vacancy.objects.all().count()
        self.assertEqual(count_before_request, count_after_request)

    def test_search_vacancies_all_filters(self) -> None:
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

        self.assertEqual(len(result), 1)
        self.assertIn("python", vacancy.name.lower())

    def test_search_vacancies_by_name(self) -> None:
        data = SearchVacancyDTO(
            name="er", company_name="", level="", expirience="", min_salary=None, max_salary=None, tag=""
        )
        result = search_vacancies(search_filters=data)

        self.assertEqual(len(result), 2)
        for vacancy in result:
            self.assertIn("er", vacancy.name.lower())

    def test_search_vacancies_by_company_name(self) -> None:
        data = SearchVacancyDTO(
            name="", company_name="google", level="", expirience="", min_salary=None, max_salary=None, tag=""
        )
        result = search_vacancies(search_filters=data)
        vacancy = result[0]

        self.assertEqual(len(result), 1)
        self.assertIn("google", vacancy.company.name.lower())
