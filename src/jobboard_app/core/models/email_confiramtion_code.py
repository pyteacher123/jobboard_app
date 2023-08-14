from django.contrib.auth import get_user_model
from django.db import models


class EmailConfirmationCodes(models.Model):
    code = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="confirmation_codes",
    )
    expiration = models.PositiveIntegerField()

    class Meta:
        db_table = "email_confirmation_codes"
