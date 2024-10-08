# Generated by Django 4.2.4 on 2023-10-26 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imdb_django.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Name",
            fields=[
                (
                    "n_const",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("primary_Name", models.CharField(max_length=255)),
                ("birth_Year", models.PositiveIntegerField(blank=True, null=True)),
                ("death_Year", models.PositiveIntegerField(blank=True, null=True)),
                ("primary_Profession", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Title",
            fields=[
                (
                    "t_const",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("title_Type", models.CharField(max_length=50)),
                ("primary_Title", models.TextField()),
                ("original_Title", models.TextField()),
                ("is_Adult", models.BooleanField()),
                ("start_Year", models.CharField(blank=True, max_length=20)),
                ("end_Year", models.CharField(blank=True, max_length=20)),
                ("runtime_Minutes", models.CharField(blank=True, max_length=20)),
                (
                    "genres",
                    models.ManyToManyField(
                        related_name="genres",
                        related_query_name="genre",
                        to="imdb_django.genre",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TitleRating",
            fields=[
                (
                    "t_const",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="ratings",
                        serialize=False,
                        to="imdb_django.title",
                    ),
                ),
                (
                    "average_Rating",
                    models.FloatField(
                        validators=[imdb_django.models.validate_float_range]
                    ),
                ),
                ("num_Votes", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="WishlistItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("t_const", models.CharField(max_length=10, unique=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wishlist_shows",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TitlePrincipal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ordering", models.PositiveIntegerField()),
                ("category", models.CharField(max_length=50)),
                ("job", models.CharField(max_length=255)),
                ("characters", models.CharField(max_length=255)),
                (
                    "n_const",
                    models.ForeignKey(
                        default="nn000001",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="principal_names",
                        to="imdb_django.name",
                    ),
                ),
                (
                    "t_const",
                    models.ForeignKey(
                        default="tt000001",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="principal",
                        to="imdb_django.title",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TitleCrew",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "directors",
                    models.ManyToManyField(
                        related_name="directed_titles",
                        related_query_name="directed_title",
                        to="imdb_django.name",
                    ),
                ),
                (
                    "t_const",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="crew",
                        to="imdb_django.title",
                    ),
                ),
                (
                    "writers",
                    models.ManyToManyField(
                        related_name="written_titles",
                        related_query_name="written_title",
                        to="imdb_django.name",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TitleAka",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ordering", models.PositiveIntegerField()),
                ("title", models.TextField()),
                ("region", models.CharField(max_length=10)),
                ("language", models.CharField(max_length=10)),
                ("types", models.CharField(max_length=255)),
                ("attributes", models.CharField(max_length=255)),
                ("is_Original_Title", models.BooleanField()),
                (
                    "t_const",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Aka",
                        to="imdb_django.title",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="name",
            name="known_For_Titles",
            field=models.ManyToManyField(
                related_name="known_for_movies",
                related_query_name="movies",
                to="imdb_django.title",
            ),
        ),
        migrations.CreateModel(
            name="TitleEpisode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("season_Number", models.PositiveIntegerField()),
                ("episode_Number", models.PositiveIntegerField()),
                (
                    "t_const",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="episodes",
                        to="imdb_django.title",
                    ),
                ),
                (
                    "title",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="season",
                        to="imdb_django.title",
                    ),
                ),
            ],
            options={
                "unique_together": {("t_const", "season_Number", "episode_Number")},
            },
        ),
    ]
