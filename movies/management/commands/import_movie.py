from django.core.management.base import BaseCommand
from movies.models import Movie, Genre
from movies.services import fetch_movies, fetch_movie_details

class Command(BaseCommand):
    help = "Import movies from TMDb"

    LANGUAGES = {
        "en": "English",
        "hi": "Hindi",
        "ml": "Malayalam",
        "ta": "Tamil",
        "te": "Telugu",
    }

    TOTAL_PAGES = 100

    def handle(self, *args, **kwargs):

        total = 0

        for code, language in self.LANGUAGES.items():

            self.stdout.write(f"\nImporting {language} movies...")

            for page in range(1, self.TOTAL_PAGES + 1):

                try:
                    movies = fetch_movies(code, page)

                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Skipping page {page}: {e}"
                        )
                    )
                    continue

                if not movies:
                    continue

                for data in movies:

                    if not data.get("poster_path"):
                        continue

                    movie, created = Movie.objects.update_or_create(

                        tmdb_id=data["id"],

                        defaults={

                            "title": data.get("title", ""),

                            "language": language,

                            "description": data.get("overview", ""),

                            "imdb_rating": data.get("vote_average", 0),

                            "release_date": data.get("release_date") or None,

                            "poster": (
                                f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
                            ),

                            "backdrop": (
                                f"https://image.tmdb.org/t/p/original{data['backdrop_path']}"
                                if data.get("backdrop_path")
                                else ""
                            ),

                            "popularity": data.get("popularity", 0),

                            "vote_count": data.get("vote_count", 0),

                            "adult": data.get("adult", False),

                        },

                    )

                    details = fetch_movie_details(data["id"])

                    for g in details.get("genres", []):

                        genre, _ = Genre.objects.get_or_create(
                            name=g["name"]
                        )

                        movie.genres.add(genre)

                    total += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"{language} completed."
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nImported/Updated {total} movies."
            )
        )