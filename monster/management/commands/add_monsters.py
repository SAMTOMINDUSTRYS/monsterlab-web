from django.core.management.base import BaseCommand, CommandError
from django.core.files import File

from monster import models

class Command(BaseCommand):
    help = 'Add a Monster Genome'
    def add_arguments(self, parser):
        parser.add_argument('filename')


    def handle(self, *args, **options):
        ref = open(options["filename"])

        last_reference = None

        for line in ref:
            line = line.strip()
            fields = line.split("\t")
            print(line)
            if len(line) == 0 or line[0] == "#":
                continue

            elif fields[0] == "R":
                last_reference = models.Reference.objects.get(pk=fields[1])

            else:
                if not last_reference:
                    raise CommandError("oh no")

                m = models.Monster(name=fields[0], reference=last_reference, scientist_name=fields[2], institute_name=fields[3])
                m.save()
                m.record_image.save(fields[4].split("/")[-1], File(open(fields[4])))
                m.annotate(fields[1])
                m.save()
                print(m.id)

