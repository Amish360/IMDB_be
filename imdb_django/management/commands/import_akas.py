import csv
import logging

from django.core.management.base import BaseCommand
from django.db import transaction
from imdb_django.models import TitleAka

# Initialize the logger
logger = logging.getLogger(__name__)

# Custom function to log detailed information
def log_info(header, data):
    logger.info(header)
    for key, value in data.items():
        logger.info(f"{key}: {value}")
    logger.info("")

class MyCommandForImportingAkasData(BaseCommand):
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
                    t_const = row["titleId"]
                    ordering = row["ordering"]
                    title = row["title"]
                    region = row["region"]
                    language = row["language"]
                    types = row["types"]
                    attributes = row["attributes"]
                    is_original_title = row["isOriginalTitle"] == "1"

                    # Create a TitleAka object
                    title_aka = TitleAka(
                        t_const=t_const,
                    )

                    title_akas_to_create.append(title_aka)

                    # Log the data for the current row
                    self.log_row_data(row_count, t_const, ordering, title, region, language, types, attributes, is_original_title)

                    row_count += 1  # Increment row count

            # Use bulk_create to insert the rows with ignore_conflicts=True
            TitleAka.objects.bulk_create(title_akas_to_create, ignore_conflicts=True)

        logger.info(f"\nData import completed. Loaded {row_count} rows.")

    def log_row_data(self, row_count, t_const, ordering, title, region, language, types, attributes, is_original_title):
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
