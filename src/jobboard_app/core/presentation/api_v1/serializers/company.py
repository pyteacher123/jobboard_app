from rest_framework import serializers


class CompanyInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    employees_number = serializers.IntegerField()
    vacancy__count = serializers.IntegerField()


class CompanySerializer(CompanyInfoSerializer):
    logo = serializers.CharField()


class CreateCompanySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30, trim_whitespace=True)
    employees_number = serializers.IntegerField(min_value=1)
    logo = serializers.ImageField(allow_empty_file=False)
