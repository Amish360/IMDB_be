# myapp/management/commands/import_title_data.py

import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from imdb_django.models import Genre, Title
from helper import log_info  # Import the log_info function


class TitleDataImportCommand(BaseCommand):
    help = "Load data from TSV file into MySQL database"

    def add_arguments(self, parser):
        parser.add_argument("tsv_file", type=str, help="Path to the TSV file")

    def handle(self, *args, **options):
        tsv_file_path = options["tsv_file"]

        with open(tsv_file_path, "r", encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t")

            with transaction.atomic():  # Use a transaction for database consistency
                row_count = 0  # Initialize a row count
                titles_to_create = []

                for row in tsv_reader:
                    title, genres_list = self.process_row(row)
                    titles_to_create.append(title)

                    if len(titles_to_create) == 1000:  # Batch insert every 1000 rows
                        Title.objects.bulk_create(titles_to_create)
                        titles_to_create.clear()

                    self.add_genres_to_title(title, genres_list)
                    row_count += 1

                # Insert any remaining titles
                if titles_to_create:
                    Title.objects.bulk_create(titles_to_create)

        # Log a message to indicate completion
        log_info(f"\nData import completed. Loaded {row_count} rows.")

    def process_row(self, row):
        genres_list = row["genres"].split(",") if row["genres"] else []

        title = Title(
            t_const=row["t_const"],
        )

        return title, genres_list

    def add_genres_to_title(self, title, genres_list):
        genres_to_create = [Genre(name=genre_name.strip()) for genre_name in genres_list]
        title.genres.set(genres_to_create)

    def log_row_data(self, row_count, row, genres_list):
        log_info(f"Loaded row {row_count}:", {
            't_const': row["t_const"],
            'title_Type': row["title_Type"],
            'primary_Title': row["primary_Title"],
            'original_Title': row["original_Title"],
            'is_Adult': row["is_Adult"],
            'startYear': row["start_Year"],
            'end_Year': row["end_Year"],
            'runtime_Minutes': row["runtime_Minutes"],
            'genres': ", ".join(genres_list),
        })
