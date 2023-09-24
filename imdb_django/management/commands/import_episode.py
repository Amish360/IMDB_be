import csv

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import IntegrityError

from imdb_django.models import Title, TitleEpisode  # Import the Title model


class Command(BaseCommand):
    help = "Load data from TSV file into MySQL database"

    def add_arguments(self, parser):
        parser.add_argument("tsv_file", type=str, help="Path to the TSV file")

    def handle(self, *args, **options):
        tsv_file_path = options["tsv_file"]

        with open(tsv_file_path, "r", encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t")

            with transaction.atomic():
                row_count = 0

                for row in tsv_reader:
                    tconst_str = row["tconst"]
                    parentTconst_str = row["parentTconst"]
                    seasonNumber = (
                        int(row["seasonNumber"])
                        if row["seasonNumber"] != "\\N"
                        else None
                    )
                    episodeNumber = (
                        int(row["episodeNumber"])
                        if row["episodeNumber"] != "\\N"
                        else None
                    )

                    try:
                        tconst_instance, _ = Title.objects.get_or_create(
                            tconst=tconst_str
                        )

                        # Retrieve or create the Title instance based on parentTconst_str
                        parentTconst_instance, _ = Title.objects.get_or_create(
                            tconst=parentTconst_str
                        )

                        title_episode, created = TitleEpisode.objects.get_or_create(
                            tconst=tconst_instance,
                            parentTconst=parentTconst_instance,  # Assign the Title instance, not the string
                            seasonNumber=seasonNumber,
                            episodeNumber=episodeNumber,
                        )
                    except IntegrityError:
                        self.stdout.write(
                            self.style.SUCCESS(f"Loaded row {row_count}:")
                        )
                        self.stdout.write(f"tconst: {tconst_str}")
                        self.stdout.write(f"parentTconst: {parentTconst_str}")
                        self.stdout.write(f"seasonNumber: {seasonNumber}")
                        self.stdout.write(f"episodeNumber: {episodeNumber}\n")

                        self.stderr.write(
                            self.style.ERROR(
                                f"Failed to load row {row_count + 1}: ForeignKey reference to Title failed"
                            )
                        )
                        continue

                    row_count += 1

                    self.stdout.write(self.style.SUCCESS(f"Loaded row {row_count}:"))
                    self.stdout.write(f"tconst: {tconst_instance.tconst}")
                    self.stdout.write(f"parentTconst: {parentTconst_instance.tconst}")
                    self.stdout.write(f"seasonNumber: {seasonNumber}")
                    self.stdout.write(f"episodeNumber: {episodeNumber}\n")

        self.stdout.write(
            self.style.SUCCESS(f"\nData import completed. Loaded {row_count} rows.")
        )
