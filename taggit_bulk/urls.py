"""Urlconf for taggit_bulk"""

from __future__ import print_function, absolute_import


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


from taggit_bulk.views import TaggitBulkWizard

app_name = 'taggit_bulk'

urlpatterns = [
    re_path(r'^wizard/$', TaggitBulkWizard.as_view(), name='wizard'),
]
