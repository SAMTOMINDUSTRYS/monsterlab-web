# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

#Event
#    uuid
#    datetime
#    location
#    name
#    description
#    sequencer ->
#    labtech

class Monster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #event
    name = models.CharField(max_length=64)
    reference = models.ForeignKey('Reference')

    monster_image = models.ImageField(upload_to="uploads/monsters/", null=True)
    record_image = models.ImageField(upload_to="uploads/monsters/", null=True)

    scientist_name = models.CharField(max_length=64)
    institute_name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    def annotate(self, sequence):
        for i, base in enumerate(sequence):
            ra = ReferenceAnnotation.objects.get(reference=self.reference, position=i+1)
            a = VariantAllele.objects.get(variant=ra.variant, sequence=base)

            mv = MonsterVariant(monster=self, allele=a)
            mv.save()

    def get_variant_allele(self, variant_uuid):
        try:
            return self.monstervariant_set.get(allele__variant__id=variant_uuid)
        except ObjectDoesNotExist:
            return None

    @property
    def alleles(self):
        alleles = []
        for mv in self.monstervariant_set.all():
            alleles.append(mv.allele)
        return alleles

class Reference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #code = models.CharField(max_length=16)
    name = models.CharField(max_length=16)
    #version

    def __str__(self):
        return self.name

    @property
    def annotated_genes(self):
        #TODO @samstudio8 This seems like it should be easier...
        genes = {}
        for a in self.referenceannotation_set.all():
            gene_effects = a.variant.effects
            for gene in gene_effects:
                if gene not in genes:
                    genes[gene] = {}
                if a.variant not in genes[gene]:
                    genes[gene][a.variant] = []
                genes[gene][a.variant].extend(gene_effects[gene])

        return genes

class ReferenceAnnotation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.ForeignKey('Reference')
    #chrom
    #start
    #end
    position = models.PositiveIntegerField()
    variant = models.ForeignKey('Variant')

    def __str__(self):
        return "%s:Chr1:%d - %s" % (self.reference.name, self.position, self.variant)

class Gene(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=8)
    name = models.CharField(max_length=32)
    desc = models.CharField(max_length=255)

    def __str__(self):
        return self.code

class Variant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return "%s" % (str(self.id)[:5])

    @property
    def effects(self):
        effects = {}
        for a in self.variantallele_set.all():
            for e in a.varianteffect_set.all():
                if e.gene.code not in effects:
                    effects[e.gene.code] = []
                effects[e.gene.code].append(e)
        return effects

class VariantAllele(models.Model):
    variant = models.ForeignKey('Variant')
    sequence = models.CharField(max_length=1)

    def __str__(self):
        return "%s : %s" % (str(self.variant.id)[:5], self.sequence)

    class Meta:
        unique_together = ('variant', 'sequence',)

class VariantEffect(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    allele = models.ForeignKey('VariantAllele')
    gene = models.ForeignKey('Gene')
    summary = models.CharField(max_length=64)
    description = models.CharField(max_length=255)

    class Meta:
        unique_together = ('gene', 'allele',)

    def __str__(self):
        return "%s:%s - %s" % (self.allele, self.gene.code, self.summary)

class MonsterVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    monster = models.ForeignKey('Monster')
    allele = models.ForeignKey('VariantAllele')

    def __str__(self):
        return "[%s] %s" % (self.allele, self.monster)


"""
Monster
    uuid
    event

    species_name
    image

    scientist name
    scientist school

    date created
    datetime uploaded

    reference
    sequence

Gene
    id
    code
    name
    description


Allele
    id
    gene
    sequence (a, aa, aaa, ac, cc, ccc, x, y whatever)
    short description
    long description

Reference
    id
    name

ReferenceAnnotation
    reference
    pos
    gene


Sequencer
    uuid
    institute


def annotate():

    annots = [r.pos for self.reference.annots]
    for i, rpos in ref:
        if i in annots:
            # special
        else:
            # not special
"""
