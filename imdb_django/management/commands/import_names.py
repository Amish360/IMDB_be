import csv

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import IntegrityError

from imdb_django.models import Name, Title


class Command(BaseCommand):
    help = "Load data from TSV file into Name model"

    def add_arguments(self, parser):
        parser.add_argument("tsv_file", type=str, help="Path to the TSV file")

    def handle(self, *args, **options):
        tsv_file_path = options["tsv_file"]

        with open(tsv_file_path, "r", encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t")

            with transaction.atomic():
                row_count = 0

                for row in tsv_reader:
                    nconst_str = row["nconst"]
                    primaryName = row["primaryName"]
                    birthYear = (
                        int(row["birthYear"]) if row["birthYear"] != "\\N" else None
                    )
                    deathYear = (
                        int(row["deathYear"]) if row["deathYear"] != "\\N" else None
                    )
                    primaryProfession = row["primaryProfession"]

                    try:
                        name, created = Name.objects.get_or_create(
                            nconst=nconst_str,
                            primaryName=primaryName,
                            birthYear=birthYear,
                            deathYear=deathYear,
                            primaryProfession=primaryProfession,
                        )

                        # Process knownForTitles (assuming it's a comma-separated list)
                        known_for_titles_str = row["knownForTitles"]
                        known_for_titles_list = known_for_titles_str.split(",")
                        for title_id in known_for_titles_list:
                            title_instance, _ = Title.objects.get_or_create(
                                tconst=title_id.strip()
                            )
                            name.knownForTitles.add(title_instance)

                    except IntegrityError:
                        self.stdout.write(
                            self.style.SUCCESS(f"Loaded row {row_count}:")
                        )
                        self.stdout.write(f"nconst: {nconst_str}")
                        self.stdout.write(f"primaryName: {primaryName}")
                        self.stdout.write(f"birthYear: {birthYear}")
                        self.stdout.write(f"deathYear: {deathYear}")
                        self.stdout.write(f"primaryProfession: {primaryProfession}")
                        self.stdout.write(f"knownForTitles: {known_for_titles_str}\n")

                        self.stderr.write(
                            self.style.ERROR(
                                f"Failed to load row {row_count + 1}: IntegrityError"
                            )
                        )
                        continue

                    row_count += 1

                    self.stdout.write(self.style.SUCCESS(f"Loaded row {row_count}:"))
                    self.stdout.write(f"nconst: {nconst_str}")
                    self.stdout.write(f"primaryName: {primaryName}")
                    self.stdout.write(f"birthYear: {birthYear}")
                    self.stdout.write(f"deathYear: {deathYear}")
                    self.stdout.write(f"primaryProfession: {primaryProfession}")
                    self.stdout.write(f"knownForTitles: {known_for_titles_str}\n")

        self.stdout.write(
            self.style.SUCCESS(f"\nData import completed. Loaded {row_count} rows.")
        )
