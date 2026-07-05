import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity

from movies.models import Movie


def recommend_movies(movie_id):

    movies = Movie.objects.all()

    data = []

    for movie in movies:

        data.append({
            "id": movie.id,
            "title": movie.title,
            "overview": movie.description
        })

    df = pd.DataFrame(data)

    tfidf = TfidfVectorizer(stop_words="english")

    tfidf_matrix = tfidf.fit_transform(df["overview"])

    similarity = cosine_similarity(tfidf_matrix)

    index = df[df["id"] == movie_id].index[0]

    scores = list(enumerate(similarity[index]))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recommendations = []

    for score in scores[1:7]:

        recommendations.append(df.iloc[score[0]].to_dict())

    return recommendations