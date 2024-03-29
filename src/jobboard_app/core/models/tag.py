from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = "tags"
