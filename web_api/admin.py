from django.contrib import admin

from web_api.models import Dataset, Detector, PreprocessedDataset, Annotation

admin.site.register(Dataset)
admin.site.register(Detector)
admin.site.register(PreprocessedDataset)
admin.site.register(Annotation)