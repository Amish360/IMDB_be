import csv
import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from imdb_django.models import Title, TitleRating

# Initialize the logger
logger = logging.getLogger(__name__)

# Custom function to log detailed information
def log_info(header, data):
    logger.info(header)
    for key, value in data.items():
        logger.info(f"{key}: {value}")
    logger.info("")

class MyCommandForImportingRatingsData(BaseCommand):
    help = "Load data from TSV file into TitleRating model"

    def add_arguments(self, parser):
        parser.add_argument("tsv_file", type=str, help="Path to the TSV file")

    def handle(self, *args, **options):
        tsv_file_path = options["tsv_file"]

        with open(tsv_file_path, "r", encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t")

            title_ratings_to_create = []

            with transaction.atomic():
                row_count = 0

                for row in tsv_reader:
                    title_ratings_to_create.append(self.process_row(row, row_count))
                    row_count += 1

                # Use bulk_create to insert the rows with ignore_conflicts=True
                TitleRating.objects.bulk_create(title_ratings_to_create, ignore_conflicts=True)

        log_info(f"\nData import completed. Loaded {row_count} rows.")

    def process_row(self, row, row_count):
        t_const = row["tconst"]
        average_Rating = float(row["averageRating"])
        num_Votes = int(row["numVotes"])

        t_const_instance, _ = self.get_or_create_title(t_const)
        return TitleRating(
            t_const=t_const_instance,
        )

    def get_or_create_title(self, tconst_str):
        return Title.objects.get_or_create(tconst=tconst_str)

    def log_row_data(self, row_count, t_const, average_Rating, num_Votes):
        log_info(f"Loaded row {row_count}:", {
            "t_const": t_const,
            "average_Rating": average_Rating,
            "num_Votes": num_Votes,
        })
