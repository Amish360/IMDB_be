import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import IntegrityError
from imdb_django.models import Title, TitleCrew, Name
from helper import log_info

class Command(BaseCommand):
    help = "Load data from TSV file into TitleCrew model"

    def add_arguments(self, parser):
        parser.add_argument("tsv_file", type=str, help="Path to the TSV file")

    def handle(self, *args, **options):
        tsv_file_path = options["tsv_file"]

        with open(tsv_file_path, "r", encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t")

            with transaction.atomic():
                row_count = 0
                name_instances = []

                for row_count, row in enumerate(tsv_reader, start=1):
                    self.process_row(row, row_count, name_instances)

                # Bulk create Name instances
                Name.objects.bulk_create(name_instances)

                self.handle_title_crew(tsv_reader, row_count)

    def process_row(self, row, row_count, name_instances):
        try:
            t_const = row["tconst"]
            director = row["directors"].split(",") if row["directors"] else []
            writer = row["writers"].split(",") if row["writers"] else []

            title_instance = self.get_or_create_title(t_const)

            # Collect Name instances for bulk_create
            name_instances.extend(self.get_or_create_names(director + writer))

            self.log_row_data(row_count, t_const, director, writer)

        except IntegrityError:
            self.log_error(f"Failed to load row {row_count}: IntegrityError occurred")
        except (ValueError, Title.DoesNotExist):
            self.log_error(f"Failed to load row {row_count}: Value error or Title does not exist")

    def handle_title_crew(self, tsv_reader, row_count):
        for row in tsv_reader:
            t_const = row["tconst"]
            director = row["directors"].split(",") if row["directors"] else []
            writer = row["writers"].split(",") if row["writers"] else []

            title_instance = self.get_or_create_title(t_const)

            directors = Name.objects.filter(n_const__in=director)
            writers = Name.objects.filter(n_const__in=writer)

            title_crew, created = TitleCrew.objects.get_or_create(t_const=title_instance)

            # Update directors and writers
            title_crew.directors.set(directors)
            title_crew.writers.set(writers)

            if created:
                self.log_success(f"Loaded row {row_count}: Created new TitleCrew")
            else:
                self.log_success(f"Loaded row {row_count}: Updated existing TitleCrew")

        self.log_success(f"\nData import completed. Loaded {row_count} rows.")

    def get_or_create_title(self, title_id):
        return Title.objects.get_or_create(t_const=title_id)[0]

    def get_or_create_names(self, n_const_list):
        return [Name(n_const=n_const) for n_const in n_const_list]


    def log_row_data(self, row_count, t_const, directors_str, writers_str):
        log_info(f"Loaded row {row_count}:", {
            "t_const": t_const,
            "directors": directors_str,
            "writers": writers_str,
        })
