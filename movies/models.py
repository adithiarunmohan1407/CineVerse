from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    tmdb_id = models.IntegerField(unique=True)
    language = models.CharField(max_length=50)
    description = models.TextField()
    imdb_rating = models.FloatField(default=0)
    release_date = models.DateField(null=True, blank=True)
    poster = models.URLField()
    backdrop = models.URLField(blank=True)
    popularity = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)

    adult = models.BooleanField(default=False)

    genres = models.ManyToManyField(Genre)

    # NEW
    liked_by = models.ManyToManyField(
        User,
        blank=True,
        related_name="liked_movies"
    )

    def __str__(self):
        return self.title