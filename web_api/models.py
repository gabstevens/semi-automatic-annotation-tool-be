from djongo import models

class Detector(models.Model):
    name = models.CharField(max_length=255)
    command = models.CharField(max_length=255)

    def __str__(self):
      return  self.name


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)

    def __str__(self):
      return  self.name