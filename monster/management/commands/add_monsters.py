from django.core.management.base import BaseCommand, CommandError
from django.core.files import File

from datetime import datetime
import os

from monster import models

class Command(BaseCommand):
    help = 'Add a Monster Genome'
    def add_arguments(self, parser):
        parser.add_argument('filename')


    def handle(self, *args, **options):
        ref = open(options["filename"])

        last_reference = None
        last_event = None
        last_dir = ""

        n = 1
        for line in ref:
            line = line.strip()
            fields = line.split("\t")
            print(line)
            if len(line) == 0 or line[0] == "#":
                continue

            elif fields[0] == "R":
                last_reference = models.Reference.objects.get(pk=fields[1])

            elif fields[0] == "E":
                last_event = models.SequencingEvent(name=fields[1], short_name=fields[2], description=fields[3], date=datetime.strptime(fields[4], "%Y-%m-%d"), location=fields[5])
                last_event.save()

            elif fields[0] == "D":
                last_dir = fields[1]

            else:
                if not last_reference:
                    raise CommandError("oh no")

                name = list(fields[0])
                name[0] = name[0].upper()
                name = "".join(name)
                m = models.Monster(name=name, reference=last_reference, scientist_name=fields[2], institute_name=fields[3], event=last_event, number=n)
                m.save()
                f_path = os.path.join(last_dir, fields[4])
                m.record_image.save(os.path.basename(f_path), File(open(f_path)))
                m.annotate(fields[1])
                m.save()
                print(m.id)
                n += 1

