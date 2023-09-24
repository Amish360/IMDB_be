# Create your models here.
from django.conf import settings
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Title(models.Model):
    tconst = models.CharField(max_length=20, primary_key=True)
    titleType = models.CharField(max_length=50)
    primaryTitle = models.TextField()
    originalTitle = models.TextField()
    isAdult = models.BooleanField()
    startYear = models.CharField(max_length=20, blank=True)
    endYear = models.CharField(max_length=20, blank=True)
    runtimeMinutes = models.CharField(max_length=20, blank=True)
    genres = models.ManyToManyField(Genre)


class TitleAka(models.Model):
    titleId = models.ForeignKey(Title, on_delete=models.CASCADE)
    ordering = models.PositiveIntegerField()
    title = models.TextField()
    region = models.CharField(max_length=10)
    language = models.CharField(max_length=10)
    types = models.CharField(max_length=255)
    attributes = models.CharField(max_length=255)
    isOriginalTitle = models.BooleanField()


class TitleCrew(models.Model):
    titleId = models.ForeignKey(Title, on_delete=models.CASCADE)
    directors = models.ManyToManyField("Name", related_name="directed_titles")
    writers = models.ManyToManyField("Name", related_name="written_titles")


class TitleEpisode(models.Model):
    tconst = models.OneToOneField(Title, primary_key=True, on_delete=models.CASCADE)
    parentTconst = models.ForeignKey(
        Title, related_name="episodes", on_delete=models.CASCADE
    )
    seasonNumber = models.PositiveIntegerField()
    episodeNumber = models.PositiveIntegerField()


class TitlePrincipal(models.Model):
    titleId = models.ForeignKey(Title, on_delete=models.CASCADE)
    ordering = models.PositiveIntegerField()
    nconst = models.ForeignKey("Name", on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    job = models.CharField(max_length=255)
    characters = models.CharField(max_length=255)


class TitleRating(models.Model):
    tconst = models.OneToOneField(Title, primary_key=True, on_delete=models.CASCADE)
    averageRating = models.FloatField()
    numVotes = models.PositiveIntegerField()


class Name(models.Model):
    nconst = models.CharField(max_length=20, primary_key=True)
    primaryName = models.CharField(max_length=255)
    birthYear = models.PositiveIntegerField(null=True, blank=True)
    deathYear = models.PositiveIntegerField(null=True, blank=True)
    primaryProfession = models.CharField(max_length=255)
    knownForTitles = models.ManyToManyField(Title, related_name="known_for_names")

    def __str__(self):
        return self.primaryName


class UserFavoriteTVShow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tv_show = models.ForeignKey(Title, on_delete=models.CASCADE)
