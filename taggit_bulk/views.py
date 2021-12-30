"""Views for taggit_bulk"""

from __future__ import print_function, absolute_import
import sys

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.admin.utils import model_ngettext
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

if tuple(sys.version_info) < (3, 0, 0):
    from django.utils.translation import ugettext_lazy as _
else:
    from django.utils.translation import gettext_lazy as _

from formtools.wizard.views import SessionWizardView

from taggit_bulk import forms, settings as default_settings
from taggit.models import Tag, TaggedItem


class TaggitBulkWizard(SessionWizardView):
    """Wizard view for taggit_bulk"""
    form_list = [forms.TaggingForm]

    def done(self, form_list, form_dict, **kw):
        """Overriden to do a job"""
        options = self.get_options()
        data = {}
        for f in form_list:
            data.update(f.cleaned_data)
        data.update(self.request.session[options['session_prefix']])
        content_type = ContentType.objects.get_by_natural_key(data['app_label'], data['model'])
        ids = data['ids']
        model = content_type.model_class()
        objs = model.objects.filter(pk__in=ids)
        ids = list(objs.values_list('pk', flat=True))
        cnt = len(ids)
        tags = [Tag.objects.get_or_create(name=t)[0] for t in data['tags']]
        existent = TaggedItem.objects.filter(tag__in=tags, content_type=content_type, object_id__in=ids)
        if data['clear']:
            existent.delete()
            messages.add_message(self.request, messages.INFO, _("Untagged %(number)s %(model_name)s") % {
                "number": cnt,
                "model_name": model_ngettext(model._meta, cnt)
            })
        else:
            existent_tags = set([(e.tag_id, e.object_id) for e in existent])
            tagged_items = [
                TaggedItem(tag=tag, content_type=content_type, object_id=o.id)
                for o in objs for tag in tags if not (tag.id, o.id) in existent_tags
            ]
            TaggedItem.objects.bulk_create(tagged_items)
            messages.add_message(self.request, messages.INFO, _("Tagged %(number)s %(model_name)s") % {
                "number": cnt,
                "model_name": model_ngettext(model._meta, cnt)
            })
        return HttpResponseRedirect(data['referer'])

    def render(self, form=None, **kw):
        options = self.get_options()
        if not options['session_prefix'] in self.request.session:
            raise PermissionDenied()
        return super(TaggitBulkWizard, self).render(form, **kw)

    def get_template_names(self):
        """Overriden to search for the special names"""
        return [
            'taggit_bulk_wizard_form.html',
            'taggit_bulk/wizard_form.html',
            'taggit_bulk/wizard/form.html',
        ]

    def get_context_data(self, form, **kw):
        """Returns additional context for the admin site template"""
        context = super(TaggitBulkWizard, self).get_context_data(form, **kw)
        options = self.get_options()
        data = {}
        data.update(self.request.session[options['session_prefix']])
        content_type = ContentType.objects.get_by_natural_key(data['app_label'], data['model'])
        model = content_type.model_class()
        context.update({
            'title': _('Bulk tagging %(number)s %(model_name)s') % {
                'model_name': model_ngettext(model._meta, len(data['ids'])),
                'number': len(data['ids'])
            },
            'site_title': admin.site.site_title,
            'site_header': admin.site.site_header,
            'index_title': admin.site.index_title,
            'has_permission': admin.site.has_permission(self.request),
            'available_apps': admin.site.get_app_list(self.request),
            'is_popup': False,
        })
        return context

    def get_options(self):
        """Returns options from settings"""
        options = {}
        options.update(getattr(default_settings, 'TAGGIT_BULK_SETTINGS', {}))
        options.update(getattr(settings, 'TAGGIT_BULK_SETTINGS', {}))
        return options
