from django import forms
from .models import ErrorLogUpload, FileUpload


class UploadForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={"class" : "form-control"}))
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))


class ErrorUploadForm(forms.ModelForm):
    class Meta:
        model = ErrorLogUpload
        fields = "__all__"


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = "__all__"


# class ErrorLogUpload(models.Model):
#     line = models.IntegerField()
#     email = models.CharField(50)
#     message = models.TextField()


# class FileUpload(models.Model):
#     name = models.CharField(max_length=50)
#     content = models.TextField()
#     count = models.IntegerField()
#     error = models.ManyToManyField(ErrorLogUpload, blank=True)
