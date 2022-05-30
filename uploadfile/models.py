from django.db import models

# Create your models here.


class ErrorLogUpload(models.Model):
    line = models.IntegerField()
    email = models.CharField(max_length=50)
    message = models.TextField()


class FileUpload(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()
    count = models.IntegerField()
    error = models.ManyToManyField(ErrorLogUpload, blank=True)
