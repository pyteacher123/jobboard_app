from core.models import Level
from core.presentation.common.validators import FileExtensionValidator, FileSizeValidator, MaxTagCountValidator
from core.presentation.web.validators import ValidateWebData
from django import forms


def get_levels() -> list:
    levels = [(level.name, level.name) for level in Level.objects.all()]
    return levels


class AddVacancyForm(forms.Form):
    name = forms.CharField(label="Name", max_length=30, strip=True)
    company_name = forms.CharField(label="Company", max_length=30, strip=True)
    level = forms.ChoiceField(label="Level", choices=get_levels())
    expirience = forms.CharField(label="Expirience", max_length=30, strip=True)
    min_salary = forms.IntegerField(label="Min Salary", min_value=0, required=False)
    max_salary = forms.IntegerField(label="Max Salary", min_value=0, required=False)
    attachment = forms.FileField(
        label="Attachment",
        allow_empty_file=False,
        validators=[
            ValidateWebData(FileExtensionValidator(["pdf"])),
            ValidateWebData(FileSizeValidator(max_size=5_000_000)),
        ],
    )
    tags = forms.CharField(
        label="Tags", widget=forms.Textarea, validators=[ValidateWebData(MaxTagCountValidator(max_count=5))]
    )


class SearchVacancyForm(forms.Form):
    template_name = "search_form_snippet.html"

    name = forms.CharField(label="Position", max_length=30, strip=True, required=False)
    company_name = forms.CharField(label="Company", max_length=30, strip=True, required=False)
    level = forms.ChoiceField(label="Level", choices=[("", "ALL")] + get_levels(), required=False)
    expirience = forms.CharField(label="Expirience", max_length=30, strip=True, required=False)
    min_salary = forms.IntegerField(label="Min Salary", min_value=0, required=False)
    max_salary = forms.IntegerField(label="Max Salary", min_value=0, required=False)
    tag = forms.CharField(label="Tag", required=False)


class ApplyVacancyForm(forms.Form):
    note = forms.CharField(label="Note", max_length=1000, widget=forms.Textarea)
    cv = forms.FileField(
        label="CV",
        allow_empty_file=False,
        validators=[
            ValidateWebData(FileExtensionValidator(["pdf"])),
            ValidateWebData(FileSizeValidator(max_size=5_000_000)),
        ],
    )
