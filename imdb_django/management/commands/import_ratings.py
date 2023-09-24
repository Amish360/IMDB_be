import csv

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import IntegrityError

from imdb_django.models import Title, TitleRating


class Command(BaseCommand):
    help = "Load data from TSV file into TitleRating model"

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
                    averageRating = float(row["averageRating"])
                    numVotes = int(row["numVotes"])

                    try:
                        tconst_instance, _ = Title.objects.get_or_create(
                            tconst=tconst_str
                        )

                        title_rating, created = TitleRating.objects.get_or_create(
                            tconst=tconst_instance,
                            averageRating=averageRating,
                            numVotes=numVotes,
                        )
                    except IntegrityError:
                        self.stdout.write(
                            self.style.SUCCESS(f"Loaded row {row_count}:")
                        )
                        self.stdout.write(f"tconst: {tconst_str}")
                        self.stdout.write(f"averageRating: {averageRating}")
                        self.stdout.write(f"numVotes: {numVotes}\n")

                        self.stderr.write(
                            self.style.ERROR(
                                f"Failed to load row {row_count + 1}: ForeignKey reference to Title failed"
                            )
                        )
                        continue

                    row_count += 1

                    self.stdout.write(self.style.SUCCESS(f"Loaded row {row_count}:"))
                    self.stdout.write(f"tconst: {tconst_instance.tconst}")
                    self.stdout.write(f"averageRating: {averageRating}")
                    self.stdout.write(f"numVotes: {numVotes}\n")

        self.stdout.write(
            self.style.SUCCESS(f"\nData import completed. Loaded {row_count} rows.")
        )
