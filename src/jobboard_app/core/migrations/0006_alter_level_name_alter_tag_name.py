# Generated by Django 4.2.2 on 2023-07-09 08:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_vacancy_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="level",
            name="name",
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(max_length=30, unique=True),
        ),
    ]