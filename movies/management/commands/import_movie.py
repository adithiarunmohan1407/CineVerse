from django.core.management.base import BaseCommand
from movies.models import Movie
from movies.services import fetch_movies


class Command(BaseCommand):
    help = "Import multilingual movies from TMDb"

    languages = {
        "en": "English",
        "hi": "Hindi",
        "ml": "Malayalam",
        "ta": "Tamil",
        "te": "Telugu",
    }

    def handle(self, *args, **kwargs):
        total = 0

        for code, name in self.languages.items():
            self.stdout.write(f"\nImporting {name} movies...")

            for page in range(1, 26):
                movies = fetch_movies(code, page)

                for movie in movies:
                    if not movie.get("poster_path"):
                        continue

                    Movie.objects.update_or_create(
                        tmdb_id=movie["id"],
                        defaults={
                            "title": movie["title"],
                            "language": name,
                            "description": movie["overview"],
                            "imdb_rating": movie["vote_average"],
                            "release_date": movie.get("release_date") or None,
                            "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                            if movie.get("poster_path")
                            else "",
                            "backdrop": f"https://image.tmdb.org/t/p/original{movie['backdrop_path']}"
                            if movie.get("backdrop_path")
                            else "",
                            "popularity": movie.get("popularity", 0),
                            "vote_count": movie.get("vote_count", 0),
                            "adult": movie.get("adult", False),
                        },
                    )
                    total += 1

        self.stdout.write(
            self.style.SUCCESS(f"\nSuccessfully imported {total} movies!")
        )
        