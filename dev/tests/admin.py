from __future__ import print_function, absolute_import

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import TaggitExample

from taggit_bulk.actions import tag_wizard


class TaggitExampleAdmin(ModelAdmin):
    list_display = ["name", "quantity", "weight", "price", "kind"]

    actions = [
        tag_wizard
    ]


admin.site.register(TaggitExample, TaggitExampleAdmin)
