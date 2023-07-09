from typing import Any

from core.models import Level
from django.db import migrations

DEFAULT_LEVELS = ("Intern", "Junior", "Middle", "Senior")


def populate_levels_table(apps: Any, schema_editor: Any) -> None:
    for level in DEFAULT_LEVELS:
        Level.objects.create(name=level)


def reverse_table_population(apps: Any, schema_editor: Any) -> None:
    for level in DEFAULT_LEVELS:
        Level.objects.get(name=level).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_level_tag_vacancy_tags_alter_vacancy_level"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_levels_table,
            reverse_code=reverse_table_population,
        )
    ]
