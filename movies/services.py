import os
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"


def fetch_movies(language="en", page=1):

    url = f"{BASE_URL}/discover/movie"

    params = {
        "api_key": API_KEY,
        "with_original_language": language,
        "sort_by": "popularity.desc",
        "page": page,
        "include_adult": False,
        "vote_count.gte": 50,
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []

    return response.json().get("results", [])


def fetch_movie_details(movie_id):

    url = f"{BASE_URL}/movie/{movie_id}"

    params = {
        "api_key": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {}

    return response.json()