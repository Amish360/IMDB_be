import csv
import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from imdb_django.models import Name, Title, TitlePrincipal

# Initialize the logger
logger = logging.getLogger(__name__)

# Custom function to log detailed information
def log_info(header, data):
    logger.info(header)
    for key, value in data.items():
        logger.info(f"{key}: {value}")
    logger.info("")

class MyCommandForImportingPrincipalsData(BaseCommand):
    help = "Load data from TSV file into TitlePrincipal model"

    def add_arguments(self, parser):
        parser.add_argument("tsv_file", type=str, help="Path to the TSV file")

    def handle(self, *args, **options):
        tsv_file_path = options["tsv_file"]

        with open(tsv_file_path, "r", encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t")

            title_principals_to_create = []

            with transaction.atomic():
                row_count = 0

                for row in tsv_reader:
                    title_principals_to_create.append(self.process_row(row, row_count))
                    row_count += 1

                # Use bulk_create to insert the rows with ignore_conflicts=True
                TitlePrincipal.objects.bulk_create(title_principals_to_create, ignore_conflicts=True)

        log_info(f"\nData import completed. Loaded {row_count} rows.")

    def process_row(self, row, row_count):
        t_const = row["tconst"]
        ordering = int(row["ordering"])
        n_const = row["nconst"]
        category = row["category"]
        job = row["job"]
        characters = row["characters"]

        title_instance, _ = self.get_or_create_title(t_const)
        name_instance, _ = self.get_or_create_name(n_const)
        job = self.truncate_job(job)

        return TitlePrincipal(
            t_const=title_instance,
        )

    def get_or_create_title(self, t_const):
        return Title.objects.get_or_create(t_const=t_const)

    def get_or_create_name(self, n_const):
        return Name.objects.get_or_create(n_const=n_const)

    def truncate_job(self, job):
        max_job_length = TitlePrincipal._meta.get_field("job").max_length
        if len(job) > max_job_length:
            self.stdout.write(self.style.WARNING(f'Truncated "job" field value. Original value: {job}'))
            job = job[:max_job_length]
        return job

    def log_row_data(self, row_count, t_const, ordering, n_const, category, job, characters):
        log_info(f"Loaded row {row_count}:", {
            "t_const": t_const,
            "ordering": ordering,
            "n_const": n_const,
            "category": category,
            "job": job,
            "characters": characters,
        })
