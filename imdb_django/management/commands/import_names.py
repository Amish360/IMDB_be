import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from imdb_django.models import Name, Title
from helper import log_info

class Command(BaseCommand):
    help = "Load data from TSV file into Name model"

    def add_arguments(self, parser):
        parser.add_argument("tsv_file", type=str, help="Path to the TSV file")

    def handle(self, *args, **options):
        tsv_file_path = options["tsv_file"]

        with open(tsv_file_path, "r", encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t")
            name_instances = []

            with transaction.atomic():
                row_count = 0

                for row_count, row in enumerate(tsv_reader, start=1):
                    name_instance = self.process_row(row)
                    if name_instance:
                        name_instances.append(name_instance)

                        # Log the data for the current row using log_row_data function
                        self.log_row_data(row_count, row)

                # Bulk create Name instances
                Name.objects.bulk_create(name_instances)

                log_info(f"\nData import completed. Loaded {row_count} rows.")

    def process_row(self, row):
        n_const = row["nconst"]
        primary_Name = row["primaryName"]
        birth_Year = int(row["birthYear"]) if row["birthYear"] != "\\N" else None
        death_Year = int(row["deathYear"]) if row["deathYear"] != "\\N" else None
        primary_Profession = row["primaryProfession"]

        name_instance = Name(
            n_const=n_const,
        )

        # Process knownForTitles (assuming it's a comma-separated list)
        known_for_titles = row["knownForTitles"]
        known_for_titles_list = known_for_titles.split(",")
        title_instances = []

        for title_id in known_for_titles_list:
            title_instance, _ = Title.objects.get_or_create(tconst=title_id.strip())
            title_instances.append(title_instance)

        name_instance.knownForTitles.set(title_instances)

        return name_instance

    def log_row_data(self, row_count, row):
        n_const = row["nconst"]
        primary_Name = row["primaryName"]
        birth_Year = int(row["birthYear"]) if row["birthYear"] != "\\N" else None
        death_Year = int(row["deathYear"]) if row["deathYear"] != "\\N" else None
        primary_Profession = row["primaryProfession"]
        known_for_titles = row["knownForTitles"]

        log_info(f"Loaded row {row_count}:", {
            "n_const": n_const,
            "primary_Name": primary_Name,
            "birth_Year": birth_Year,
            "death_Year": death_Year,
            "primary_Profession": primary_Profession,
            "knownForTitles": known_for_titles,
        })

    def log_success(self, message):
        log_info(message)

    def log_error(self, message):
        log_info(message)
