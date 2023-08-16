from django.contrib.auth import get_user_model
from django.db import models


class JobResponse(models.Model):
    vacancy = models.ForeignKey(to="Vacancy", on_delete=models.CASCADE, related_name="job_responses")
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="job_responses")
    note = models.CharField(max_length=1000)
    cv = models.FileField(upload_to="users/cvs/", null=True)

    class Meta:
        db_table = "job_responses"
