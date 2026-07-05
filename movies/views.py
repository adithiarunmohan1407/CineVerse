from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Movie
from recommender.utils import recommend


def landing(request):
    return render(request, "landing.html")


@login_required(login_url="login")
def home(request):

    movies = Movie.objects.all()

    search = request.GET.get("search")
    language = request.GET.get("language")
    rating = request.GET.get("rating")
    year = request.GET.get("year")

    if search:
        movies = movies.filter(title__icontains=search)

    if language:
        movies = movies.filter(language=language)

    if rating:
        movies = movies.filter(imdb_rating__gte=rating)

    if year:
        movies = movies.filter(release_date__year=year)

    paginator = Paginator(movies, 20)

    page = request.GET.get("page")

    page_obj = paginator.get_page(page)

    return render(request, "home.html", {
        "movies": page_obj,
        "page_obj": page_obj,
    })


@login_required(login_url="login")
def movie_detail(request, id):

    movie = get_object_or_404(Movie, id=id)

    try:
        recommendations = recommend(movie.id)
    except:
        recommendations = []

    return render(request, "movie_detail.html", {
        "movie": movie,
        "recommendations": recommendations,
    })


@login_required(login_url="login")
def wishlist(request):
    return render(request, "wishlist.html")


@login_required(login_url="login")
def add_to_wishlist(request, id):

    movie = get_object_or_404(Movie, id=id)

    messages.success(request, f"{movie.title} added to wishlist!")

    return redirect("movie_detail", id=id)