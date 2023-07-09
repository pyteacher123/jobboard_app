from django.db import models


class Company(models.Model):
    name = models.CharField(unique=True, max_length=100)
    employees_number = models.PositiveIntegerField()

    class Meta:
        db_table = "companies"


class Vacancy(models.Model):
    level = models.ForeignKey(to="Level", on_delete=models.CASCADE, related_name="vacancy")
    expirience = models.CharField(max_length=30)
    min_salary = models.PositiveIntegerField(null=True)
    max_salary = models.PositiveIntegerField(null=True)
    company = models.ForeignKey(
        to="Company", on_delete=models.CASCADE, related_name="vacancies", related_query_name="vacancy"
    )
    tags = models.ManyToManyField(to="Tag", related_name="vacancies", db_table="vacancies_tags")
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "vacancies"


class Level(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = "levels"


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = "tags"
