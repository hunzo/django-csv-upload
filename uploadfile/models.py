from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ErrorLogUpload(models.Model):
    ref_id = models.CharField(max_length=50)
    line = models.IntegerField()
    email = models.CharField(max_length=50)
    error_message = models.TextField()

    def __str__(self):
        return self.ref_id


class FileUpload(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    count = models.IntegerField()
    error = models.ManyToManyField(ErrorLogUpload, blank=True)
    ref_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
