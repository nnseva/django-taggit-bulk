from __future__ import print_function, absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager


class TaggitExample(models.Model):
    """ Import Example """

    name = models.CharField(
        max_length=128,
        verbose_name=_('Name'),
    )
    quantity = models.IntegerField(
        null=True, blank=True,
        verbose_name=_('Quantity'),
    )
    weight = models.FloatField(
        null=True, blank=True,
        verbose_name=_('Weight'),
    )
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True, blank=True,
        verbose_name=_('Price'),
    )
    kind = models.CharField(
        max_length=32,
        choices=[
            ('wood', _('Wood')),
            ('steel', _('Steel')),
            ('oil', _('Oil')),
        ],
        verbose_name=_('Kind'),
    )

    tags = TaggableManager(
        blank=True,
        verbose_name=_('Tags'), help_text=_('A comma-separated list of tags')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Taggit Example')
        verbose_name_plural = _('Taggit Examples')
