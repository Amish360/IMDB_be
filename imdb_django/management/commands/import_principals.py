import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import IntegrityError, DataError
from imdb_django.models import Title, TitlePrincipal, Name
from helper import log_info

class Command(BaseCommand):
    help = "Load data from TSV file into TitlePrincipal model"

    def add_arguments(self, parser):
        parser.add_argument("tsv_file", type=str, help="Path to the TSV file")

    def handle(self, *args, **options):
        tsv_file_path = options["tsv_file"]

        with open(tsv_file_path, "r", encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t")

            with transaction.atomic():
                title_principals_to_create = []
                row_count = 0

                for row_count, row in enumerate(tsv_reader, start=1):
                    title_principal = self.process_row(row,row_count)
                    if title_principal:
                        title_principals_to_create.append(title_principal)

                # Bulk create TitlePrincipal instances
                TitlePrincipal.objects.bulk_create(title_principals_to_create)

                log_info(f"\nData import completed. Loaded {row_count} rows.")

    def process_row(self, row, row_count):
        t_const = row["tconst"]
        ordering = int(row["ordering"])
        n_const = row["nconst"]
        category = row["category"]
        job = row["job"]
        characters = row["characters"]

        title_instance = self.get_or_create_title(t_const)
        name_instance = self.get_or_create_name(n_const)

        self.log_row_data(row_count, t_const, ordering, n_const, category, job, characters)

        try:
            title_principal = TitlePrincipal(
                t_const=title_instance,
                n_const=name_instance,
            )
        except DataError:
            log_info(f"Skipped: DataError occurred. Skipping row due to 'job' field length.")
            return None

        return title_principal

    def get_or_create_title(self, t_const):
        try:
            return Title.objects.get(t_const=t_const)
        except Title.DoesNotExist:
            log_info(f"Failed to load row: Title with t_const {t_const} does not exist")
            return None

    def get_or_create_name(self, n_const):
        try:
            return Name.objects.get(n_const=n_const)
        except Name.DoesNotExist:
            log_info(f"Failed to load row: Name with n_const {n_const} does not exist")
            return None

    def log_info(self, message):
        log_info(message)

    def log_row_data(self, row_count, t_const, ordering, n_const, category, job, characters):
        log_info(f"Loaded row {row_count}:", {
            "t_const": t_const,
            "ordering": ordering,
            "n_const": n_const,
            "category": category,
            "job": job,
            "characters": characters,
        })
