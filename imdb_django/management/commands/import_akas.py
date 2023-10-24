import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from imdb_django.models import TitleAka  # Replace 'myapp' with the actual app name
from helper import log_info  # Import the log_info function

class AkasDataImportCommand(BaseCommand):
    help = "Load data from TSV file into MySQL database"

    def add_arguments(self, parser):
        parser.add_argument("tsv_file", type=str, help="Path to the TSV file")

    def handle(self, *args, **options):
        tsv_file_path = options["tsv_file"]

        with open(tsv_file_path, "r", encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t")

            title_akas_to_create = []

            with transaction.atomic():  # Use a transaction for database consistency
                row_count = 0  # Initialize a row count

                for row in tsv_reader:
                    self.process_row(row, title_akas_to_create, row_count)
                    row_count += 1

            # Use bulk_create to insert the rows with ignore_conflicts=True
            TitleAka.objects.bulk_create(title_akas_to_create, ignore_conflicts=True)

        # Log a message to indicate completion
        log_info(f"Data import completed. Loaded {row_count} rows.")

    def process_row(self, row, title_akas_to_create, row_count):
        t_const = row["titleId"]
        ordering = row["ordering"]
        title = row["title"]
        region = row["region"]
        language = row["language"]
        types = row["types"]
        attributes = row["attributes"]
        is_original_title = row["isOriginalTitle"] == "1"

        # Create a TitleAka object and append it to the list
        title_aka = TitleAka(
            t_const=t_const,
        )
        title_akas_to_create.append(title_aka)

        # Log the data for the current row using log_info function
        log_info(f"Loaded row {row_count}:", {
            "t_const": t_const,
            "ordering": ordering,
            "title": title,
            "region": region,
            "language": language,
            "types": types,
            "attributes": attributes,
            "is_Original_Title": is_original_title,
        })
