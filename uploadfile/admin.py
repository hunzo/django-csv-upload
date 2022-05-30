from django.contrib import admin
from .models import FileUpload, ErrorLogUpload

# Register your models here.

admin.site.register(FileUpload)
admin.site.register(ErrorLogUpload)