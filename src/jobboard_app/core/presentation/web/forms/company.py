from core.presentation.common.validators import (
    FileExtensionValidator,
    FileSizeValidator,
    validate_swear_words_in_company_name,
)
from core.presentation.web.validators import ValidateWebData
from django import forms


class AddCompanyForm(forms.Form):
    name = forms.CharField(
        label="Company", max_length=30, strip=True, validators=[ValidateWebData(validate_swear_words_in_company_name)]
    )
    employees_number = forms.IntegerField(label="Employees", min_value=1)
    logo = forms.ImageField(
        label="Logo",
        allow_empty_file=False,
        validators=[
            ValidateWebData(FileExtensionValidator(["png", "jpg", "jpeg"])),
            ValidateWebData(FileSizeValidator(max_size=5_000_000)),
        ],
    )
