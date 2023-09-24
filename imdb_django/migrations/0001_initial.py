# Generated by Django 4.2.4 on 2023-09-03 18:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

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
                    "nconst",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("primaryName", models.CharField(max_length=255)),
                ("birthYear", models.PositiveIntegerField(blank=True, null=True)),
                ("deathYear", models.PositiveIntegerField(blank=True, null=True)),
                ("primaryProfession", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Title",
            fields=[
                (
                    "tconst",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("titleType", models.CharField(max_length=50)),
                ("primaryTitle", models.TextField()),
                ("originalTitle", models.TextField()),
                ("isAdult", models.BooleanField()),
                ("startYear", models.CharField(blank=True, max_length=20)),
                ("endYear", models.CharField(blank=True, max_length=20)),
                ("runtimeMinutes", models.CharField(blank=True, max_length=20)),
                ("genres", models.ManyToManyField(to="imdb_django.genre")),
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
                ("titleId", models.TextField()),
                ("ordering", models.PositiveIntegerField()),
                ("title", models.CharField(max_length=255)),
                ("region", models.CharField(max_length=10)),
                ("language", models.CharField(max_length=10)),
                ("types", models.CharField(max_length=255)),
                ("attributes", models.CharField(max_length=255)),
                ("isOriginalTitle", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="TitleRating",
            fields=[
                (
                    "tconst",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="imdb_django.title",
                    ),
                ),
                ("averageRating", models.FloatField()),
                ("numVotes", models.PositiveIntegerField()),
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
                    "nconst",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="imdb_django.name",
                    ),
                ),
                (
                    "titleId",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
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
                        related_name="directed_titles", to="imdb_django.name"
                    ),
                ),
                (
                    "titleId",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="imdb_django.title",
                    ),
                ),
                (
                    "writers",
                    models.ManyToManyField(
                        related_name="written_titles", to="imdb_django.name"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="name",
            name="knownForTitles",
            field=models.ManyToManyField(
                related_name="known_for_names", to="imdb_django.title"
            ),
        ),
        migrations.CreateModel(
            name="TitleEpisode",
            fields=[
                (
                    "tconst",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="imdb_django.title",
                    ),
                ),
                ("seasonNumber", models.PositiveIntegerField()),
                ("episodeNumber", models.PositiveIntegerField()),
                (
                    "parentTconst",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="episodes",
                        to="imdb_django.title",
                    ),
                ),
            ],
        ),
    ]