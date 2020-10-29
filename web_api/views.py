from web_api.models import Detector, Dataset
from rest_framework import viewsets
from rest_framework import permissions
from web_api.serializers import DetectorSerializer, DatasetSerializer


class DetectorViewSet(viewsets.ModelViewSet):
    queryset = Detector.objects.all()
    serializer_class = DetectorSerializer
    # permission_classes = [permissions.IsAuthenticated]


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    # permission_classes = [permissions.IsAuthenticated]