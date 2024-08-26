import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from imdb_django.models import Genre, Title
from helper import log_info

class Command(BaseCommand):
    help = "Load data from TSV file into MySQL database"

    def add_arguments(self, parser):
        parser.add_argument("tsv_file", type=str, help="Path to the TSV file")

    def handle(self, *args, **options):
        tsv_file_path = options["tsv_file"]

        with open(tsv_file_path, "r", encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t")

            with transaction.atomic():
                titles_to_create = []

                for row_count, row in enumerate(tsv_reader, start=1):
                    title = self.process_row(row, row_count)
                    if title:
                        titles_to_create.append(title)

                # Bulk create Title instances
                Title.objects.bulk_create(titles_to_create)

                log_info(f"\nData import completed. Loaded {row_count} rows.")

    def process_row(self, row, row_count):
        genres_list = row["genres"].split(",") if row["genres"] else []

        title, created = Title.objects.get_or_create(
            t_const=row["tconst"],
            title_Type=row["titleType"],
            primary_Title=row["primaryTitle"],
            original_Title=row["originalTitle"],
            is_Adult=row["isAdult"] == "1",
            start_Year=row["startYear"],
            end_Year=row["endYear"],
            runtime_Minutes=row["runtimeMinutes"],
        )

        for genre_name in genres_list:
            genre, _ = Genre.objects.get_or_create(name=genre_name.strip())
            title.genres.add(genre)

        log_info(f"Loaded row {row_count}:")
        log_info(f't_const: {row["tconst"]}')
        log_info(f'titleType: {row["titleType"]}')
        log_info(f'primaryTitle: {row["primaryTitle"]}')
        log_info(f'originalTitle: {row["originalTitle"]}')
        log_info(f'isAdult: {row["isAdult"]}')
        log_info(f'startYear: {row["startYear"]}')
        log_info(f'endYear: {row["endYear"]}')
        log_info(f'runtimeMinutes: {row["runtimeMinutes"]}')
        log_info(f'genres: {", ".join(genres_list)}\n')

        return title

