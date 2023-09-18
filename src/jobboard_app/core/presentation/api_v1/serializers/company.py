from core.presentation.api_v1.validators import ValidateAPIData
from core.presentation.common.validators import (
    FileExtensionValidator,
    FileSizeValidator,
    validate_swear_words_in_company_name,
)
from rest_framework import serializers


class CompanyInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    employees_number = serializers.IntegerField()
    vacancy__count = serializers.IntegerField()


class CompanySerializer(CompanyInfoSerializer):
    logo = serializers.CharField()


class CreateCompanySerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=30, trim_whitespace=True, validators=[ValidateAPIData(validate_swear_words_in_company_name)]
    )
    employees_number = serializers.IntegerField(min_value=1)
    logo = serializers.ImageField(
        allow_empty_file=False,
        validators=[
            ValidateAPIData(FileExtensionValidator(["png", "jpg", "jpeg"])),
            ValidateAPIData(FileSizeValidator(max_size=5_000_000)),
        ],
    )


class CreateCompanyResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    company_id = serializers.IntegerField()
