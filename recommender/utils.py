from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from movies.models import Movie


def recommend(movie_id, limit=10):

    movies = list(Movie.objects.all())

    if len(movies) < 2:
        return []

    features = []

    for movie in movies:

        genres = " ".join(
            movie.genres.values_list("name", flat=True)
        )

        text = (
            (movie.description or "") + " " +
            (movie.language or "") + " " +
            genres + " " +
            str(movie.imdb_rating)
        )

        features.append(text)

    tfidf = TfidfVectorizer(stop_words="english")

    matrix = tfidf.fit_transform(features)

    similarity = cosine_similarity(matrix)

    index = None

    for i, movie in enumerate(movies):
        if movie.id == movie_id:
            index = i
            break

    if index is None:
        return []

    scores = list(enumerate(similarity[index]))

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for movie_index, score in scores[1:]:

        movie = movies[movie_index]

        if movie.id != movie_id:
            recommendations.append(movie)

        if len(recommendations) >= limit:
            break

    return recommendations