# myapp/management/commands/import_crew_data.py

import csv
import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from imdb_django.models import Name, Title, TitleCrew
from helper import log_info  # Import the log_info function


class CrewDataImportCommand(BaseCommand):
    help = "Load data from TSV file into TitleCrew model"

    def add_arguments(self, parser):
        parser.add_argument("tsv_file", type=str, help="Path to the TSV file")

    def handle(self, *args, **options):
        tsv_file_path = options["tsv_file"]

        with open(tsv_file_path, "r", encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t")

            title_crew_data = []

            with transaction.atomic():
                row_count = 0

                for row in tsv_reader:
                    title_crew_data.append(self.process_row(row, row_count))
                    row_count += 1

                # Use bulk_create to insert or update the rows with ignore_conflicts=True
                TitleCrew.objects.bulk_create(title_crew_data, ignore_conflicts=True)

        # Log a message to indicate completion
        log_info(f"Data import completed. Loaded {row_count} rows.")

    def process_row(self, row, row_count):
        t_const = row["tconst"]

        title_instance, _ = Title.objects.get_or_create(t_const=t_const)

        # Process directors and writers
        directors_str = row["directors"]
        directors_list = directors_str.split(",")
        directors = Name.objects.filter(n_const__in=directors_list)

        writers_str = row["writers"]
        writers_list = writers_str.split(",")
        writers = Name.objects.filter(n_const__in=writers_list)

        # Log the data for the current row using log_info function
        self.log_row_data(row_count, t_const, directors_str, writers_str)

        return TitleCrew(t_const=title_instance, directors=directors, writers=writers)

    def log_row_data(self, row_count, t_const, directors_str, writers_str):
        log_info(f"Loaded row {row_count}:", {
            "t_const": t_const,
            "directors": directors_str,
            "writers": writers_str,
        })
