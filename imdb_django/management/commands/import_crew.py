import csv

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import IntegrityError

from imdb_django.models import Name, Title, TitleCrew


class Command(BaseCommand):
    help = "Load data from TSV file into TitleCrew model"

    def add_arguments(self, parser):
        parser.add_argument("tsv_file", type=str, help="Path to the TSV file")

    def handle(self, *args, **options):
        tsv_file_path = options["tsv_file"]

        with open(tsv_file_path, "r", encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t")

            with transaction.atomic():
                row_count = 0

                for row in tsv_reader:
                    title_id_str = row["tconst"]

                    try:
                        title_instance, _ = Title.objects.get_or_create(
                            tconst=title_id_str
                        )

                        # Process directors (assuming it's a comma-separated list)
                        directors_str = row["directors"]
                        directors_list = directors_str.split(",")
                        directors = Name.objects.filter(nconst__in=directors_list)

                        # Process writers (assuming it's a comma-separated list)
                        writers_str = row["writers"]
                        writers_list = writers_str.split(",")
                        writers = Name.objects.filter(nconst__in=writers_list)

                        title_crew, created = TitleCrew.objects.get_or_create(
                            titleId=title_instance
                        )

                        title_crew.directors.set(directors)
                        title_crew.writers.set(writers)

                    except IntegrityError:
                        self.stdout.write(
                            self.style.SUCCESS(f"Loaded row {row_count}:")
                        )
                        self.stdout.write(f"titleId: {title_id_str}")
                        self.stdout.write(f"directors: {directors_str}")
                        self.stdout.write(f"writers: {writers_str}\n")

                        self.stderr.write(
                            self.style.ERROR(
                                f"Failed to load row {row_count + 1}: IntegrityError"
                            )
                        )
                        continue

                    row_count += 1

                    self.stdout.write(self.style.SUCCESS(f"Loaded row {row_count}:"))
                    self.stdout.write(f"titleId: {title_id_str}")
                    self.stdout.write(f"directors: {directors_str}")
                    self.stdout.write(f"writers: {writers_str}\n")

        self.stdout.write(
            self.style.SUCCESS(f"\nData import completed. Loaded {row_count} rows.")
        )
