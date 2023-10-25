import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import IntegrityError
from imdb_django.models import Title, TitleRating
from helper import log_info

class Command(BaseCommand):
    help = "Load data from TSV file into TitleRating model"

    def add_arguments(self, parser):
        parser.add_argument("tsv_file", type=str, help="Path to the TSV file")

    def handle(self, *args, **options):
        tsv_file_path = options["tsv_file"]

        with open(tsv_file_path, "r", encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t")

            with transaction.atomic():
                title_ratings_to_create = []

                for row_count, row in enumerate(tsv_reader, start=1):
                    title_rating = self.process_row(row, row_count)
                    if title_rating:
                        title_ratings_to_create.append(title_rating)

                # Bulk create TitleRating instances
                TitleRating.objects.bulk_create(title_ratings_to_create)

                log_info(f"\nData import completed. Loaded {row_count} rows.")

    def process_row(self, row, row_count):
        t_const = row["tconst"]
        average_Rating = float(row["averageRating"])
        num_Votes = int(row["numVotes"])

        try:
            t_const_instance = self.get_or_create_title(t_const)

            title_rating, created = TitleRating.objects.update_or_create(
                t_const=t_const_instance,
            )

        except IntegrityError:
            log_info(f"Failed to load a row {t_const}: ForeignKey reference to Title failed")
            return None
        self.log_row_data(row_count, t_const, average_Rating, num_Votes)
        return title_rating

    def get_or_create_title(self, t_const):
        try:
            return Title.objects.get(t_const=t_const)
        except Title.DoesNotExist:
            log_info(f"Failed to load a row: Title with t_const {t_const} does not exist")
            return None

    def log_row_data(self, row_count, t_const, average_Rating, num_Votes):
        log_info(f"Loaded row {row_count}:", {
            "t_const": t_const,
            "average_Rating": average_Rating,
            "num_Votes": num_Votes,
        })
