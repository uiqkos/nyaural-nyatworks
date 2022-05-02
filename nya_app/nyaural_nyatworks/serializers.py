from rest_framework import serializers

from .models import *


class ReportSerializer(serializers.ModelSerializer):
    tags = serializers.ListField()

    class Meta:
        model = Report
        fields = '__all__'


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'
