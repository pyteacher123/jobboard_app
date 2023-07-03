from django import forms

from .validators import validate_swear_words_in_company_name

LEVELS = (
    ("Intern", "Intern"),
    ("Junior", "Junior"),
    ("Middle", "Middle"),
    ("Senior", "Senior"),
)


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
