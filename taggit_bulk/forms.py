"""Forms for taggit_bulk"""

from __future__ import print_function, absolute_import
import sys

from django import forms
from taggit.forms import TagField

if tuple(sys.version_info) < (3, 0, 0):
    from django.utils.translation import ugettext_lazy as _
else:
    from django.utils.translation import gettext_lazy as _


class TaggingForm(forms.Form):
    """A bulk tagging wizard form"""
    tags = TagField(label=_("Tags"), help_text=_("Input tags to be added or cleared depending on the <b>Clear</b> flag"))
    clear = forms.BooleanField(required=False, label=_("Clear"), help_text=_("Whether to clear these tags instead of adding them"))
