from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import authenticate

if TYPE_CHECKING:
    from core.business_logic.dto import LoginDTO
    from django.contrib.auth.models import AbstractBaseUser

from core.business_logic.exceptions import InvalidAuthCredentials


def authenticate_user(data: LoginDTO) -> AbstractBaseUser:
    user = authenticate(username=data.username, password=data.password)
    if user is not None:
        return user
    else:
        raise InvalidAuthCredentials
