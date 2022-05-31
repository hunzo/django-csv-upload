from django.urls import path
from .views import home, valid_generate_csv, invalid_generate_csv

urlpatterns = [
    path("", home, name="home"),
    path("download/valid", valid_generate_csv, name="valid_download"),
    path("download/invalid", invalid_generate_csv, name="invalid_download")
]
