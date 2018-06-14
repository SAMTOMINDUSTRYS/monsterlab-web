# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class SequencingEvent(models.Model):
    name = models.CharField(max_length=64, unique=True, db_index=True)
    description = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=64)
#    sequencer ->
#    labtech

    def __str__(self):
        return self.name

class Monster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    event = models.ForeignKey('SequencingEvent')
    number = models.PositiveIntegerField(db_index=True)

    name = models.CharField(max_length=64)
    reference = models.ForeignKey('Reference')

    monster_image = models.ImageField(upload_to="monsters/", null=True)
    record_image = models.ImageField(upload_to="monsters/", null=True)

    scientist_name = models.CharField(max_length=64)
    institute_name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('event', 'number',)

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
    def fa_name(self):
        return "%s_%s" % (self.name.replace(" ", "_"), str(self.id)[-5:])

    @property
    def alleles(self):
        alleles = []
        for mv in self.monstervariant_set.all():
            alleles.append(mv.allele)
        return alleles

    @property
    def sequence(self):
        reference = []
        alleles = []
        for a in self.reference.referenceannotation_set.order_by('position'):
            reference.append( a )
            alleles.append( self.get_variant_allele(a.variant.id) )

        seq_str = "".join([a.allele.sequence for a in alleles])
        return {"ref": reference, "seq": alleles, "seq_str": seq_str}


    @property
    def binarize(self):
        bnn = []
        for a in self.reference.referenceannotation_set.order_by('position'):
            mv = self.get_variant_allele(a.variant.id)
            alleles = [a.sequence for a in mv.allele.variant.variantallele_set.all().order_by('sequence')]
            b = [0] * len(alleles)
            b[ alleles.index(mv.allele.sequence) ] = 1

            for e in mv.allele.variant.effects:
                bnn.extend(b) 

        return ",".join([str(x) for x in bnn])



class Reference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #code = models.CharField(max_length=16)
    name = models.CharField(max_length=16)
    #version

    def __str__(self):
        return self.name

    @property
    def matrix(self):
        es = []
        for a in self.referenceannotation_set.order_by('position'):
            for gene, effects in a.variant.effects.items():
                for e in effects:
                    es.append(e.summary.replace(" ", ""))
        return ",".join(es)


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

    @property
    def prev(self):
        return ReferenceAnnotation.objects.filter(reference=self.reference, position__lt=self.position).order_by('position').last()

    @property
    def next(self):
        return ReferenceAnnotation.objects.filter(reference=self.reference, position__gt=self.position).order_by('position').first()

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

    @property
    def proportion(self):
        try:
            p = MonsterVariant.objects.filter(allele__variant=self.variant, allele__sequence=self.sequence).count() / float(MonsterVariant.objects.filter(allele__variant=self.variant).count()) * 100
        except ZeroDivisionError:
            return 0
        return "%.2f" % p

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
