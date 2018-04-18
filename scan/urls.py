from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^simple_upload', views.simple_upload, name='simple_upload'),
]
