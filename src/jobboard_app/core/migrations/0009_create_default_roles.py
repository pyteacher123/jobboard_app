from typing import Any

from django.contrib.auth.models import Group
from django.db import migrations

DEFAULT_ROLES = ["candidate", "recruiter"]


def populate_db_with_default_roles(apps: Any, schema_editor: Any) -> None:
    for role_name in DEFAULT_ROLES:
        Group.objects.create(name=role_name)


def drop_default_roles_from_db(apps: Any, schema_editor: Any) -> None:
    for role_name in DEFAULT_ROLES:
        Group.objects.get(name=role_name).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_company_logo"),
    ]

    operations = [migrations.RunPython(code=populate_db_with_default_roles, reverse_code=drop_default_roles_from_db)]
