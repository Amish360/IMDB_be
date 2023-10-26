import csv
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from imdb_django.models import Title, TitleAka
from helper import log_info

class AkasDataImportCommand(BaseCommand):
    help = "Load data from TSV file into TitleAka model"

    def add_arguments(self, parser):
        parser.add_argument("tsv_file", type=str, help="Path to the TSV file")

    def handle(self, *args, **options):
        tsv_file_path = options["tsv_file"]
        title_akas_to_create = []  # Collect TitleAka instances for bulk_create

        with open(tsv_file_path, "r", encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t")

            for row_count, row in enumerate(tsv_reader, start=1):
                title_aka = self.process_row(row, row_count)
                if title_aka:
                    title_akas_to_create.append(title_aka)

            # Bulk create the TitleAka instances
            TitleAka.objects.bulk_create(title_akas_to_create)

            log_info(
                f"\nData import completed. Loaded {row_count} rows."
            )

    def process_row(self, row, row_count):
        t_const = row["titleId"]
        ordering = int(row["ordering"])
        title_text = row["title"]
        region = row["region"]
        language = row["language"]
        types = row["types"]
        attributes = row["attributes"]
        is_original_title = row["isOriginalTitle"].lower() == "true"

        try:
            title_instance = self.get_or_create_title(t_const)

            title_aka = TitleAka(
                t_const=title_instance,
            )

            log_info(f"Loaded row {row_count}:", {
                "t_const": t_const,
                "ordering": ordering,
                "title": title_text,
                "region": region,
                "language": language,
                "types": types,
                "attributes": attributes,
                "is_original_title": is_original_title,
            })

            return title_aka
        except IntegrityError:
            self.handle_integrity_error(row_count)

    def get_or_create_title(self, title_id):
        return Title.objects.get(tconst=title_id)

    def handle_integrity_error(self, row_count):
        log_info(f"Failed to load row {row_count}: IntegrityError occurred")
