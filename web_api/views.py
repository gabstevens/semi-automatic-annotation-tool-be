from web_api.models import Detector, Dataset, PreprocessedDataset, Annotation
from rest_framework import viewsets
from rest_framework import permissions
from web_api.serializers import DetectorSerializer, DatasetSerializer, PreprocessedDatasetSerializer, AnnotationSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django_q.tasks import async_task
import json

class DetectorViewSet(viewsets.ModelViewSet):
    queryset = Detector.objects.all()
    serializer_class = DetectorSerializer
    # permission_classes = [permissions.IsAuthenticated]

class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    # permission_classes = [permissions.IsAuthenticated]

class PreprocessedDatasetViewSet(viewsets.ModelViewSet):
    queryset = PreprocessedDataset.objects.all()
    serializer_class = PreprocessedDatasetSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    # permission_classes = [permissions.IsAuthenticated]

@csrf_exempt
def preprocess(request):
    data = json.loads(request.body.decode('utf-8'))["preprocessed_dataset"]
    dataset = Dataset.objects.get(id=data["dataset_id"])
    detector = Detector.objects.get(id=data["detector_id"])
    preprocessed_dataset = PreprocessedDataset(dataset=dataset, detector=detector, name=data["name"])
    preprocessed_dataset.save()
    async_task("web_api.services.detect_async", preprocessed_dataset=preprocessed_dataset, is_both=data["is_both"])
    return JsonResponse({})