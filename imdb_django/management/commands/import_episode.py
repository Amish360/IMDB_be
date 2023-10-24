# myapp/management/commands/import_episode_data.py

import csv
import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from imdb_django.models import Title, TitleEpisode
from helper import log_info  # Import the log_info function

# Initialize the logger
logger = logging.getLogger(__name)

class EpisodeDataImportCommand(BaseCommand):
    help = "Load data from TSV file into MySQL database"

    def add_arguments(self, parser):
        parser.add_argument("tsv_file", type=str, help="Path to the TSV file")

    def handle(self, *args, **options):
        tsv_file_path = options["tsv_file"]

        with open(tsv_file_path, "r", encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t")

            title_episodes_to_create = []

            with transaction.atomic():
                row_count = 0

                for row in tsv_reader:
                    title_episodes_to_create.append(self.process_row(row, row_count))
                    row_count += 1

                # Use bulk_create to insert or update the rows with ignore_conflicts=True
                TitleEpisode.objects.bulk_create(title_episodes_to_create, ignore_conflicts=True)

        # Log a message to indicate completion
        log_info(f"Data import completed. Loaded {row_count} rows.")

    def process_row(self, row, row_count):
        t_const = row["tconst"]
        title = row["parentTconst"]
        season_Number = (
            int(row["seasonNumber"])
            if row["seasonNumber"] != "\\N"
            else None
        )
        episode_Number = (
            int(row["episodeNumber"])
            if row["episodeNumber"] != "\\N"
            else None
        )

        title_instance, _ = self.get_or_create_title(t_const)
        title_parent_instance, _ = self.get_or_create_title_parent(title)

        # Log the data for the current row using log_info function
        self.log_row_data(row_count, t_const, title_instance, season_Number, episode_Number)

        return TitleEpisode(
            t_const=title_instance,
            title=title_parent_instance,
            season_Number=season_Number,
            episode_Number=episode_Number,
        )

    def get_or_create_title(self, t_const):
        return Title.objects.get_or_create(tconst=t_const)

    def get_or_create_title_parent(self, title):
        return Title.objects.get_or_create(tconst=title)

    def log_row_data(self, row_count, t_const, title, season_Number, episode_Number):
        log_info(f"Loaded row {row_count}:", {
            "t_const": t_const.t_const,
            "parent_T_const": title.t_const,
            "season_Number": season_Number,
            "episode_Number": episode_Number,
        })
