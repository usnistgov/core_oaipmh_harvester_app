""" Url router for the main application
"""
from django.conf.urls import include
from django.urls import re_path

urlpatterns = [
    re_path(r"^rest/", include("core_oaipmh_harvester_app.rest.urls")),
]
