"""Actions for the bulk_taggit"""

from __future__ import print_function, absolute_import

from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from taggit_bulk import settings as default_settings


def tag_wizard(admin, request, queryset):
    """The action starts tagging wizard"""
    options = {}
    options.update(getattr(default_settings, 'TAGGIT_BULK_SETTINGS', {}))
    options.update(getattr(settings, 'TAGGIT_BULK_SETTINGS', {}))
    request.session[options['session_prefix']] = {
        'app_label': queryset.model._meta.app_label,
        'model': queryset.model._meta.model_name,
        'ids': [o.pk for o in queryset],
        'referer': request.path,
    }
    return HttpResponseRedirect(reverse('taggit_bulk:wizard'))


tag_wizard.short_description = _("Bulk tag/untag selected objects")
