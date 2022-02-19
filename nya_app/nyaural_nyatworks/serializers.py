from rest_framework import serializers

from .models import *


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = '__all__'
