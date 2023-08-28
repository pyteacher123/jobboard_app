from rest_framework import serializers


class SearchVacanciesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30, trim_whitespace=True, required=False, default="")
    company_name = serializers.CharField(max_length=30, trim_whitespace=True, required=False, default="")
    level = serializers.CharField(max_length=30, trim_whitespace=True, required=False, default="")
    expirience = serializers.CharField(max_length=30, trim_whitespace=True, required=False, default="")
    min_salary = serializers.IntegerField(min_value=0, required=False, default=None)
    max_salary = serializers.IntegerField(min_value=0, required=False, default=None)
    tag = serializers.CharField(required=False, default="")


class CompanyInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class LevelInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class VacancyInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    company = CompanyInfoSerializer()
    level = LevelInfoSerializer()
    expirience = serializers.CharField()
    min_salary = serializers.IntegerField()
    max_salary = serializers.IntegerField()
