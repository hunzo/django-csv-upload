from django.contrib import admin
from .models import FileUpload, ErrorLogUpload

# Register your models here.

class FileUploadAdmin(admin.ModelAdmin):
    list_display =  ("name", "author", "count", "ref_id")

class ErrorLogUploadAdmin(admin.ModelAdmin):
    list_display = ("ref_id", "line", "email", "error_message")

admin.site.register(FileUpload, FileUploadAdmin)
admin.site.register(ErrorLogUpload, ErrorLogUploadAdmin)