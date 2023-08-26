from typing import Any

from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    DEFAULT_ROLES = {"candidate": [], "recruiter": ["add_vacancy", "add_company"]}

    def handle(self, *args: Any, **kwargs: Any) -> None:
        for role_name, permissions_list in self.DEFAULT_ROLES.items():
            group = Group.objects.get(name=role_name)
            permissions = Permission.objects.filter(codename__in=permissions_list)
            group.permissions.set(permissions)
            self.stdout.write(f"Added permissions for role: {role_name}")
