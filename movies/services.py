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
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get("results", [])

    return []