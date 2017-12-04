from django.core.management.base import BaseCommand, CommandError

from monster import models

class Command(BaseCommand):
    help = 'Add a Monster Genome'
    def add_arguments(self, parser):
        parser.add_argument('filename')


    def handle(self, *args, **options):
        ref = open(options["filename"])

        new_variants = []
        new_genes = []
        new_references = []

        last_effect = None

        for line in ref:
            line = line.strip()
            fields = line.split("\t")
            if len(line) == 0 or line[0] == "#":
                continue

            elif line[0] == "V":
                v = models.Variant()
                v.save()
                new_variants.append(v)

            elif line[0] == "G":
                g = models.Gene(code=fields[1], name=fields[2], desc=fields[3])
                g.save()
                new_genes.append(g)

            elif line[0] == "E":
                last_variant = new_variants[int(fields[1])]
                last_gene = new_genes[int(fields[2])]

            elif line[0] == "*":
                if not last_variant or not last_gene:
                    raise CommandError("grumble")

                a = models.VariantAllele(variant=last_variant, sequence=fields[1])
                a.save()

                e = models.VariantEffect(gene=last_gene, allele=a, summary=fields[2], description=fields[2])
                e.save()

            elif line[0] == "R":
                r = models.Reference(name=fields[1])
                print(r.id)
                r.save()

                new_references.append(r)

            elif line[0] == "A":
                ra = models.ReferenceAnnotation(reference=new_references[int(fields[1])], position=int(fields[3]), variant=new_variants[int(fields[4])])
                ra.save()
