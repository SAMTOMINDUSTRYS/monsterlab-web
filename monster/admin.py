# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models

admin.site.register(models.Monster)
admin.site.register(models.Reference)
admin.site.register(models.ReferenceAnnotation)
admin.site.register(models.Variant)
admin.site.register(models.Gene)
admin.site.register(models.VariantAllele)
admin.site.register(models.VariantEffect)
admin.site.register(models.MonsterVariant)

