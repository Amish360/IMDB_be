# myapp/management/commands/import_name_data.py

import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from imdb_django.models import Name, Title
from helper import log_info

class NameDataImportCommand(BaseCommand):
    help = "Load data from TSV file into Name model"

    def add_arguments(self, parser):
        parser.add_argument("tsv_file", type=str, help="Path to the TSV file")

    def handle(self, *args, **options):
        tsv_file_path = options["tsv_file"]

        with open(tsv_file_path, "r", encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t")

            name_data_to_create = []

            with transaction.atomic():
                row_count = 0

                for row in tsv_reader:
                    name_data_to_create.append(self.process_row(row, row_count))
                    row_count += 1

                # Use bulk_create to insert the rows with ignore_conflicts=True
                Name.objects.bulk_create(name_data_to_create, ignore_conflicts=True)

        # Log a message to indicate completion
        log_info(f"\nData import completed. Loaded {row_count} rows.")

    def process_row(self, row, row_count):
        n_const = row["nconst"]
        primaryName = row["primaryName"]
        birthYear = int(row["birthYear"]) if row["birthYear"] != "\\N" else None
        deathYear = int(row["deathYear"]) if row["deathYear"] != "\\N" else None
        primary_Profession = row["primaryProfession"]
        known_for_titles_str = row["knownForTitles"]

        name_instance, _ = self.get_or_create_name(n_const)
        self.process_known_for_titles(name_instance, known_for_titles_str)

        return Name(
            n_const=n_const,
        )

    def get_or_create_name(self, n_const):
        return Name.objects.get_or_create(n_const=n_const)

    def process_known_for_titles(self, name_instance, known_for_titles_str):
        known_for_titles_list = known_for_titles_str.split(",")
        title_instances = Title.objects.filter(t_const__in=known_for_titles_list)
        for title_instance in title_instances:
            _, created = Title.objects.get_or_create(name=name_instance, title=title_instance)

    def log_row_data(self, row_count, n_const, primary_Name, birth_Year, death_Year, primary_Profession, known_For_Titles):
        log_info(f"Loaded row {row_count}:", {
            "n_const": n_const,
            "primary_Name": primary_Name,
            "birth_Year": birth_Year,
            "death_Year": death_Year,
            "primary_Profession": primary_Profession,
            "known_For_Titles": known_For_Titles,
        })
