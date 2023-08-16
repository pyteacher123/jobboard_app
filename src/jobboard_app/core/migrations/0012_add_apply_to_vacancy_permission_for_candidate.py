from typing import Any

from django.contrib.auth.models import Group, Permission
from django.db import migrations

DEFAULT_ROLES = {"candidate": [], "recruiter": ["add_vacancy", "add_company"]}


def add_permission_to_candidate(apps: Any, schema_editor: Any) -> None:
    group = Group.objects.get(name="candidate")
    permissions = Permission.objects.filter(codename="apply_to_vacancy")
    group.permissions.set(permissions)


def drop_permission(apps: Any, schema_editor: Any) -> None:
    group = Group.objects.get(name="candidate")
    permission = Permission.objects.get(codename="apply_to_vacancy")
    group.permissions.remove(permission)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_alter_vacancy_options"),
    ]

    operations = [migrations.RunPython(code=add_permission_to_candidate, reverse_code=drop_permission)]
