# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from . import models

def index(request):
    return HttpResponse("Hello, world. You're at the monsterlab index.")

def list(request):
    monsters = models.Monster.objects.all()

    return render(request, 'monster/list.html', {
        "monsters": monsters,
    })

def detail(request, monster_uuid):
    monster = get_object_or_404(models.Monster, pk=monster_uuid)

    # Fetch the annotations in order
    reference = []
    alleles = []
    for a in monster.reference.referenceannotation_set.order_by('position'):
        reference.append( a )
        alleles.append( monster.get_variant_allele(a.variant.id) )

    return render(request, 'monster/detail.html', {
        "monster": monster,
        "annotations": zip(reference, alleles),
    })
