"""Urlconf for taggit_bulk"""

from __future__ import print_function, absolute_import
from django.conf.urls import url

from taggit_bulk.views import TaggitBulkWizard

app_name = 'taggit_bulk'

urlpatterns = [
    url(r'^wizard/$', TaggitBulkWizard.as_view(), name='wizard'),
]
