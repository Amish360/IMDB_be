import csv

from django.core.management.base import BaseCommand
from django.db import transaction

from imdb_django.models import Genre, Title  # Import your models


class Command(BaseCommand):
    help = "Load data from TSV file into MySQL database"

    def add_arguments(self, parser):
        parser.add_argument("tsv_file", type=str, help="Path to the TSV file")

    def handle(self, *args, **options):
        tsv_file_path = options["tsv_file"]

        with open(tsv_file_path, "r", encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t")

            with transaction.atomic():  # Use a transaction for database consistency
                row_count = 0  # Initialize a row count

                for row in tsv_reader:
                    genres_list = row["genres"].split(",") if row["genres"] else []

                    title, created = Title.objects.get_or_create(
                        tconst=row["tconst"],
                        titleType=row["titleType"],
                        primaryTitle=row["primaryTitle"],
                        originalTitle=row["originalTitle"],
                        isAdult=row["isAdult"] == "1",
                        startYear=row["startYear"],
                        endYear=row["endYear"],
                        runtimeMinutes=row["runtimeMinutes"],
                    )

                    for genre_name in genres_list:
                        genre, _ = Genre.objects.get_or_create(name=genre_name.strip())
                        title.genres.add(genre)

                    row_count += 1  # Increment row count

                    # Print the data for the current row
                    self.stdout.write(self.style.SUCCESS(f"Loaded row {row_count}:"))
                    self.stdout.write(f'tconst: {row["tconst"]}')
                    self.stdout.write(f'titleType: {row["titleType"]}')
                    self.stdout.write(f'primaryTitle: {row["primaryTitle"]}')
                    self.stdout.write(f'originalTitle: {row["originalTitle"]}')
                    self.stdout.write(f'isAdult: {row["isAdult"]}')
                    self.stdout.write(f'startYear: {row["startYear"]}')
                    self.stdout.write(f'endYear: {row["endYear"]}')
                    self.stdout.write(f'runtimeMinutes: {row["runtimeMinutes"]}')
                    self.stdout.write(f'genres: {", ".join(genres_list)}\n')

        self.stdout.write(
            self.style.SUCCESS(f"\nData import completed. Loaded {row_count} rows.")
        )
