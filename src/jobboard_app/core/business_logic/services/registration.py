from __future__ import annotations

import logging
import time
import uuid
from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.urls import reverse

if TYPE_CHECKING:
    from django.contrib.auth.models import User
    from core.business_logic.dto import RegistrationDTO

from core.business_logic.exceptions import ConfirmationCodeExpired, ConfirmationCodeNotExists
from core.models import EmailConfirmationCodes

logger = logging.getLogger(__name__)


# Create user (is_active = False)
# Set role to created user
# Send email notification to the user email.

# |backend| -> |email|
# |generate code logic| -> |Aefeewfdfef|
# |Aefeewfdfef| -> |Database (EmailConfimationCodes)|
# |email| -> |http://127.0.0.1:8000/confirmation?code=Aefeewfdfef|
# |confirmation_controller| -> |business_logic| -> |set user is_active to True|


def create_user(data: RegistrationDTO) -> None:
    logger.info("Get user creation request.", extra={"user": str(data)})

    user_model: User = get_user_model()
    created_user = user_model.objects.create_user(
        username=data.username, password=data.password, email=data.email, is_active=False
    )

    group = Group.objects.get(name=data.role)
    created_user.groups.add(group)

    confirmation_code = str(uuid.uuid4())
    code_expiration_time = int(time.time()) + settings.CONFIRMATION_CODE_LIFETIME
    EmailConfirmationCodes.objects.create(code=confirmation_code, user=created_user, expiration=code_expiration_time)

    confirmation_url = settings.SERVER_HOST + reverse("confirm-signup") + f"?code={confirmation_code}"
    send_mail(
        subject="Confirm your email",
        message=f"Please confirm email by clicking the link below:\n\n{confirmation_url}",
        from_email=settings.EMAIL_FROM,
        recipient_list=[data.email],
    )


def confirm_user_registration(confirmation_code: str) -> None:
    try:
        code_data = EmailConfirmationCodes.objects.get(code=confirmation_code)
    except EmailConfirmationCodes.DoesNotExist as err:
        logger.error("Provided code doesn't exists.", exc_info=err, extra={"code": confirmation_code})
        raise ConfirmationCodeNotExists

    if time.time() > code_data.expiration:
        logger.info(
            "Provided expiration code expired.",
            extra={"current_time": str(time.time()), "code_expiration": str(code_data.expiration)},
        )
        raise ConfirmationCodeExpired

    user = code_data.user
    user.is_active = True
    user.save()

    code_data.delete()
