from django.urls import include, path
from rest_framework import routers
from web_api import views

router = routers.DefaultRouter()
router.register(r'detectors', views.DetectorViewSet)
router.register(r'datasets', views.DatasetViewSet)
router.register(r'preprocessed_datasets', views.PreprocessedDatasetViewSet)
router.register(r'annotations', views.AnnotationViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
    path('preprocess', views.preprocess, name='preprocess')
]