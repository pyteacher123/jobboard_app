from core.models import Level
from core.validators import ValidateMaxTagCount, validate_swear_words_in_company_name
from django import forms

LEVELS = [(level.name, level.name) for level in Level.objects.all()]


class AddCompanyForm(forms.Form):
    name = forms.CharField(
        label="Company", max_length=30, strip=True, validators=[validate_swear_words_in_company_name]
    )
    employees_number = forms.IntegerField(label="Employees", min_value=1)


class AddVacancyForm(forms.Form):
    name = forms.CharField(label="Name", max_length=30, strip=True)
    company_name = forms.CharField(label="Company", max_length=30, strip=True)
    level = forms.ChoiceField(label="Level", choices=LEVELS)
    expirience = forms.CharField(label="Expirience", max_length=30, strip=True)
    min_salary = forms.IntegerField(label="Min Salary", min_value=0, required=False)
    max_salary = forms.IntegerField(label="Max Salary", min_value=0, required=False)
    tags = forms.CharField(label="Tags", widget=forms.Textarea, validators=[ValidateMaxTagCount(max_count=5)])


class SearchVacancyForm(forms.Form):
    name = forms.CharField(label="Position", max_length=30, strip=True, required=False)
    company_name = forms.CharField(label="Company", max_length=30, strip=True, required=False)
    level = forms.ChoiceField(label="Level", choices=[("", "ALL")] + LEVELS, required=False)
    expirience = forms.CharField(label="Expirience", max_length=30, strip=True, required=False)
    min_salary = forms.IntegerField(label="Min Salary", min_value=0, required=False)
    max_salary = forms.IntegerField(label="Max Salary", min_value=0, required=False)
    tag = forms.CharField(label="Tag", required=False)
