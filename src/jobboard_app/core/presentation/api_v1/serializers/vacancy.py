from rest_framework import serializers


class SearchVacanciesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30, trim_whitespace=True, required=False, default="")
    company_name = serializers.CharField(max_length=30, trim_whitespace=True, required=False, default="")
    level = serializers.CharField(max_length=30, trim_whitespace=True, required=False, default="")
    expirience = serializers.CharField(max_length=30, trim_whitespace=True, required=False, default="")
    min_salary = serializers.IntegerField(min_value=0, required=False, default=None)
    max_salary = serializers.IntegerField(min_value=0, required=False, default=None)
    tag = serializers.CharField(required=False, default="")


class CompanyShortInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class LevelInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class VacancyInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    company = CompanyShortInfoSerializer()
    level = LevelInfoSerializer()
    expirience = serializers.CharField()
    min_salary = serializers.IntegerField()
    max_salary = serializers.IntegerField()


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class VacancySerializer(VacancyInfoSerializer):
    tags = TagSerializer(many=True, read_only=True)


class VacancyInfoPaginatedResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    results = VacancyInfoSerializer(many=True)
