import csv

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import IntegrityError  # Import IntegrityError

from imdb_django.models import (
    TitleAka,
)  # Replace 'your_app_name' with your actual app name


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
                    title_id = row["titleId"]
                    ordering = row["ordering"]
                    title = row["title"]
                    region = row["region"]
                    language = row["language"]
                    types = row["types"]
                    attributes = row["attributes"]
                    is_original_title = row["isOriginalTitle"] == "1"

                    try:
                        title_aka, created = TitleAka.objects.get_or_create(
                            titleId_id=title_id,
                            ordering=ordering,
                            title=title,
                            region=region,
                            language=language,
                            types=types,
                            attributes=attributes,
                            isOriginalTitle=is_original_title,
                        )
                    except IntegrityError:
                        self.stdout.write(
                            self.style.SUCCESS(f"Loaded row {row_count}:")
                        )
                        self.stdout.write(f"titleId: {title_id}")
                        self.stdout.write(f"ordering: {ordering}")
                        self.stdout.write(f"title: {title}")
                        self.stdout.write(f"region: {region}")
                        self.stdout.write(f"language: {language}")
                        self.stdout.write(f"types: {types}")
                        self.stdout.write(f"attributes: {attributes}")
                        self.stdout.write(f"isOriginalTitle: {is_original_title}\n")

                        # Handle the case where the foreign key reference fails
                        self.stderr.write(
                            self.style.ERROR(
                                f"Failed to load row {row_count + 1}: ForeignKey reference to Title failed"
                            )
                        )
                        continue

                    row_count += 1  # Increment row count

                    # Print the data for the current row
                    self.stdout.write(self.style.SUCCESS(f"Loaded row {row_count}:"))
                    self.stdout.write(f"titleId: {title_id}")
                    self.stdout.write(f"ordering: {ordering}")
                    self.stdout.write(f"title: {title}")
                    self.stdout.write(f"region: {region}")
                    self.stdout.write(f"language: {language}")
                    self.stdout.write(f"types: {types}")
                    self.stdout.write(f"attributes: {attributes}")
                    self.stdout.write(f"isOriginalTitle: {is_original_title}\n")

        self.stdout.write(
            self.style.SUCCESS(f"\nData import completed. Loaded {row_count} rows.")
        )
