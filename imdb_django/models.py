# Create your models here.
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        app_label = 'genre_app'

    def __str__(self):
        return self.name


class Title(models.Model):
    t_const = models.CharField(max_length=20, primary_key=True)
    title_Type = models.CharField(max_length=50)
    primary_Title = models.TextField()
    original_Title = models.TextField()
    is_Adult = models.BooleanField()
    start_Year = models.CharField(max_length=20, blank=True)
    end_Year = models.CharField(max_length=20, blank=True)
    runtime_Minutes = models.CharField(max_length=20, blank=True)
    genres = models.ManyToManyField(Genre, related_name='genres')

    class Meta:
        app_label = 'title_app'

    def __str__(self):
        return f"{self.title_Type} ({self.primary_Title}) ({self.original_Title}) ({self.is_Adult}) ({self.start_Year}) ({self.end_Year}) ({self.runtime_Minutes}) ({self.genres})"


class TitleAka(models.Model):
    t_const = models.ForeignKey(Title, related_name='Aka', on_delete=models.CASCADE)
    ordering = models.PositiveIntegerField()
    title = models.TextField()
    region = models.CharField(max_length=10)
    language = models.CharField(max_length=10)
    types = models.CharField(max_length=255)
    attributes = models.CharField(max_length=255)
    is_Original_Title = models.BooleanField()

    class Meta:
        app_label = 'aka_app'

    def __str__(self):
        return f"{self.ordering} ({self.title}) ({self.region}) ({self.language}) ({self.types}) ({self.attributes}) ({self.is_Original_Title})"


class TitleCrew(models.Model):
    t_const = models.ForeignKey(Title, related_name='crew', on_delete=models.CASCADE)
    directors = models.ManyToManyField("Name", related_name="directed_titles")
    writers = models.ManyToManyField("Name", related_name="written_titles")

    class Meta:
        app_label = 'crew_app'

    def __str__(self):
        return f"{self.directors} ({self.writers})"


class TitleEpisode(models.Model):
    t_const = models.OneToOneField(Title, primary_key=True, related_name='episodes', on_delete=models.CASCADE)
    title = models.ForeignKey(
        Title, related_name="episodes", on_delete=models.CASCADE
    )
    season_Number = models.PositiveIntegerField(unique=True)
    episode_Number = models.PositiveIntegerField(unique=True)

    class Meta:
        app_label = 'episode_app'

    def __str__(self):
        return f"{self.t_const} ({self.title}) ({self.season_Number}) ({self.episode_Number})"


class TitlePrincipal(models.Model):
    t_const = models.ForeignKey(Title, related_name='principal', on_delete=models.CASCADE)
    ordering = models.PositiveIntegerField()
    n_const = models.ForeignKey("Name", related_name='principal_names', on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    job = models.CharField(max_length=255)
    characters = models.CharField(max_length=255)

    class Meta:
        app_label = 'principal_app'

    def __str__(self):
        return f"{self.ordering} ({self.characters}) ({self.category}) ({self.job})"


def validate_float_range(value):
    if value < 0.0 or value > 10.0:
        raise ValidationError("Value must be between 0 and 10")


class TitleRating(models.Model):
    t_const = models.OneToOneField(Title, primary_key=True, related_name='ratings', on_delete=models.CASCADE)
    average_Rating = models.FloatField(validators=[validate_float_range])
    num_Votes = models.PositiveIntegerField()

    class Meta:
        app_label = 'ratings_app'

    def __str__(self):
        return f"{self.t_const} ({self.average_Rating}) ({self.num_Votes})"


class Name(models.Model):
    n_const = models.CharField(max_length=20, primary_key=True)
    primary_Name = models.CharField(max_length=255)
    birth_Year = models.PositiveIntegerField(null=True, blank=True)
    death_Year = models.PositiveIntegerField(null=True, blank=True)
    primary_Profession = models.CharField(max_length=255)
    known_For_Titles = models.ManyToManyField(Title, related_name="known_for_names")

    class Meta:
        app_label = 'name_app'

    def __str__(self):
        return f"{self.primary_Name} ({self.birth_Year}) ({self.death_Year}) ({self.primary_Profession}) ({self.known_For_Titles})"


class UserFavoriteTVShow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tv_show = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        app_label = 'user_fav_app'

    def __str__(self):
        return f"{self.user} ({self.tv_show})"
