import csv

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import DataError, IntegrityError

from imdb_django.models import Name, Title, TitlePrincipal


class Command(BaseCommand):
    help = "Load data from TSV file into TitlePrincipal model"

    def add_arguments(self, parser):
        parser.add_argument("tsv_file", type=str, help="Path to the TSV file")

    def handle(self, *args, **options):
        tsv_file_path = options["tsv_file"]

        with open(tsv_file_path, "r", encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t")

            with transaction.atomic():
                row_count = 0

                for row in tsv_reader:
                    title_id_str = row["tconst"]
                    ordering = int(row["ordering"])
                    nconst_str = row["nconst"]
                    category = row["category"]
                    job = row["job"]
                    characters = row["characters"]

                    try:
                        title_instance, _ = Title.objects.get_or_create(
                            tconst=title_id_str
                        )
                        name_instance, _ = Name.objects.get_or_create(nconst=nconst_str)

                        # Truncate the 'job' field value if it's too long
                        max_job_length = TitlePrincipal._meta.get_field(
                            "job"
                        ).max_length
                        if len(job) > max_job_length:
                            self.stdout.write(
                                self.style.WARNING(
                                    f'Row {row_count + 1}: Truncated "job" field value. Original value: {job}'
                                )
                            )
                            job = job[:max_job_length]

                        title_principal, created = TitlePrincipal.objects.get_or_create(
                            titleId=title_instance,
                            ordering=ordering,
                            nconst=name_instance,
                            category=category,
                            job=job,
                            characters=characters,
                        )

                    except IntegrityError:
                        self.stdout.write(
                            self.style.SUCCESS(f"Loaded row {row_count}:")
                        )
                        self.stdout.write(f"titleId: {title_id_str}")
                        self.stdout.write(f"ordering: {ordering}")
                        self.stdout.write(f"nconst: {nconst_str}")
                        self.stdout.write(f"category: {category}")
                        self.stdout.write(f"job: {job}")
                        self.stdout.write(f"characters: {characters}\n")

                        self.stderr.write(
                            self.style.ERROR(
                                f"Failed to load row {row_count + 1}: IntegrityError"
                            )
                        )
                        continue
                    except DataError:
                        self.stdout.write(
                            self.style.SUCCESS(f"Loaded row {row_count}:")
                        )
                        self.stdout.write(f"titleId: {title_id_str}")
                        self.stdout.write(f"ordering: {ordering}")
                        self.stdout.write(f"nconst: {nconst_str}")
                        self.stdout.write(f"category: {category}")
                        self.stdout.write(f"characters: {characters}\n")

                        self.stderr.write(
                            self.style.ERROR(
                                f'Failed to load row {row_count + 1}: DataError - "job" value too long.'
                            )
                        )
                        continue

                    row_count += 1

                    self.stdout.write(self.style.SUCCESS(f"Loaded row {row_count}:"))
                    self.stdout.write(f"titleId: {title_id_str}")
                    self.stdout.write(f"ordering: {ordering}")
                    self.stdout.write(f"nconst: {nconst_str}")
                    self.stdout.write(f"category: {category}")
                    self.stdout.write(f"job: {job}")
                    self.stdout.write(f"characters: {characters}\n")

        self.stdout.write(
            self.style.SUCCESS(f"\nData import completed. Loaded {row_count} rows.")
        )
