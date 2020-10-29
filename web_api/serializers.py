from web_api.models import Detector, Dataset
from rest_framework import serializers

class DetectorSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Detector
        fields = ['id', 'name', 'command']

class DatasetSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Dataset
        fields = ['id', 'name', 'path']