from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.contrib.auth.models import User
from datetime import timedelta

class Detector(models.Model):
    name = models.CharField(max_length=255)
    command = models.CharField(max_length=255)
    class_list = ArrayField(base_field=models.CharField(max_length=255), default=list)
    is_both = models.BooleanField(default=False)
    def __str__(self):
      return  self.name


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    rgb_path = models.CharField(null=True, blank=True, max_length=255)
    thermal_path = models.CharField(null=True, blank=True, max_length=255)
    def __str__(self):
      return  self.name

class PreprocessedDataset(models.Model):
    PENDING = 'PE'
    FAILED = 'FA'
    SUCCEEDED = 'SU'
    STATUS_CHOICES = [
        (PENDING, 'pending'),
        (FAILED, 'failed'),
        (SUCCEEDED, 'succeeded'),
    ]
    dataset = models.ForeignKey(Dataset, null=True, on_delete=models.SET_NULL)
    detector = models.ForeignKey(Detector, null=True, on_delete=models.SET_NULL)
    name = models.CharField(default="", max_length=255)
    time = models.DurationField(default=timedelta())
    status = models.TextField(max_length=2, choices=STATUS_CHOICES, default=PENDING)
    def __str__(self):
      return self.name

class Annotation(models.Model):
  preprocessed_dataset = models.ForeignKey(PreprocessedDataset, on_delete=models.CASCADE)
  thermal_boxes = JSONField(null=True, blank=True)
  rgb_boxes = JSONField(null=True, blank=True)
  thermal_url = models.CharField(null=True, blank=True, max_length=255)
  rgb_url = models.CharField(null=True, blank=True, max_length=255)
  checker = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
  def __str__(self):
    return f'{self.preprocessed_dataset.name} - {self.id}'