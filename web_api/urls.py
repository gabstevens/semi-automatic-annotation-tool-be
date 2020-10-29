from django.urls import include, path
from rest_framework import routers
from web_api import views

router = routers.DefaultRouter()
router.register(r'detectors', views.DetectorViewSet)
router.register(r'datasets', views.DatasetViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls))
]