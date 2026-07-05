import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity

from movies.models import Movie

def build_similarity_matrix():

    movies = Movie.objects.all()

    data = []

    for movie in movies:

        data.append({

            "id": movie.id,

            "title": movie.title,

            "overview": movie.description or "",

            "language": movie.language or "",

            "rating": str(movie.imdb_rating),

        })

    df = pd.DataFrame(data)

    df["features"] = (

        df["overview"]

        + " "

        + df["language"]

        + " "

        + df["rating"]

    )

    tfidf = TfidfVectorizer(stop_words="english")

    matrix = tfidf.fit_transform(df["features"])

    similarity = cosine_similarity(matrix)

    return df, similarity



def recommend(movie_id):

    movies = Movie.objects.all()

    data = []

    for movie in movies:

        data.append({
            "id": movie.id,
            "title": movie.title,
            "overview": movie.description or "",
            "language": movie.language or "",
            "rating": movie.imdb_rating,
            "poster": movie.poster,
        })

    df = pd.DataFrame(data)

    df["features"] = (
        df["overview"] + " " +
        df["language"]
    )

    tfidf = TfidfVectorizer(stop_words="english")

    matrix = tfidf.fit_transform(df["features"])

    similarity = cosine_similarity(matrix)

    index = df[df["id"] == movie_id].index[0]

    scores = list(enumerate(similarity[index]))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recommendations = []

    for score in scores[1:11]:
        recommendations.append(df.iloc[score[0]].to_dict())

    return recommendations