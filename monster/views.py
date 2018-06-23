# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from . import models

def index(request):
    return HttpResponse("Hello, world. You're at the monsterlab index.")

def home(request):
    monsters = models.Monster.objects.all().order_by('?')
    events = models.SequencingEvent.objects.all().order_by("-date")

    return render(request, 'monster/home.html', {
        "monsters": monsters,
        "events": events,
        "n_labs": len(events),
        "n_monsters": len(monsters),
    })

def list_event(request, event_name):
    event = get_object_or_404(models.SequencingEvent, name=event_name)
    monsters = models.Monster.objects.all().filter(event__name=event_name)
    events = models.SequencingEvent.objects.all().order_by("-date")

    return render(request, 'monster/event.html', {
        "monsters": monsters,
        "event": event,
        "events": events,
        "n_labs": 1,
        "n_monsters": len(monsters),
    })

def detail(request, monster_uuid):
    monster = get_object_or_404(models.Monster, pk=monster_uuid)

    # Fetch the annotations in order
    reference = []
    alleles = []
    for a in monster.reference.referenceannotation_set.order_by('position'):
        reference.append( a )
        alleles.append( monster.get_variant_allele(a.variant.id) )

    print "hello", events
    return render(request, 'monster/detail.html', {
        "monster": monster,
        "annotations": zip(reference, alleles),
    })

def detail2(request, event_name, monster_num):
    event = get_object_or_404(models.SequencingEvent, name=event_name)
    monster = get_object_or_404(models.Monster, event=event, number=monster_num)
    events = models.SequencingEvent.objects.all().order_by("-date")

    # Fetch the annotations in order
    reference = []
    alleles = []
    for a in monster.reference.referenceannotation_set.order_by('position'):
        reference.append( a )
        alleles.append( monster.get_variant_allele(a.variant.id) )

    return render(request, 'monster/detail.html', {
        "monster": monster,
        "annotations": zip(reference, alleles),
        "populations": events,
    })

def list_monster_allele(request, variant_uuid, allele=None):

    if allele:
        allele = models.VariantAllele.objects.get(variant_id=variant_uuid, sequence=allele)
    else:
        allele = models.VariantAllele.objects.filter(variant_id=variant_uuid).first()

    monsters = []
    for mv in allele.monstervariant_set.all():
        monsters.append( mv.monster )

    loci = {}
    for annot in models.ReferenceAnnotation.objects.filter(variant_id=variant_uuid):
        loci[annot.reference.name] = (annot.prev, annot, annot.next)

    return render(request, 'monster/allele.html', {
        "allele": allele,
        "monsters": monsters,
        "loci": loci,
    })

def list_monster_hallele(request, variant_uuid, allele=None):

    if allele:
        allele = models.VariantAllele.objects.get(variant_id=variant_uuid, sequence=allele)
    else:
        allele = models.VariantAllele.objects.filter(variant_id=variant_uuid).first()

    monsters = []
    for mv in allele.monstervariant_set.all():
        monsters.append( mv.monster )

    loci = {}
    for annot in models.ReferenceAnnotation.objects.filter(variant_id=variant_uuid):
        loci[annot.reference.name] = (annot.prev, annot, annot.next)

    return render(request, 'monster/hallele.html', {
        "allele": allele,
        "monsters": monsters,
        "loci": loci,
    })

def fasta(request):
    monsters = models.Monster.objects.all()

    return render(request, 'monster/fasta.html', {
        "monsters": monsters,
    })

def matrix(request):

    reference = models.Reference.objects.all().first()
    monsters = models.Monster.objects.filter(reference=reference)

    return render(request, 'monster/matrix.html', {
        "reference": reference,
        "monsters": monsters,
    })

def matrix2(request):

    reference = models.Reference.objects.all().first()
    monsters = models.Monster.objects.filter(reference=reference)

    return render(request, 'monster/matrix2.html', {
        "reference": reference,
        "monsters": monsters,
    })
