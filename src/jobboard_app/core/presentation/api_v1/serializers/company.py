from rest_framework import serializers


class CompanyInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    employees_number = serializers.IntegerField()
    vacancy__count = serializers.IntegerField()
