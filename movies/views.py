from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Movie, Wishlist
from recommender.utils import recommend


# ----------------------------------------
# Landing Page
# ----------------------------------------

def landing(request):
    return render(request, "landing.html")


# ----------------------------------------
# Home Page
# ----------------------------------------

@login_required(login_url="login")
def home(request):

    movies = Movie.objects.all().order_by("-popularity")

    search = request.GET.get("search")
    language = request.GET.get("language")
    rating = request.GET.get("rating")
    year = request.GET.get("year")

    if search:
        movies = movies.filter(title__icontains=search)

    if language:
        movies = movies.filter(language__iexact=language)

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


# ----------------------------------------
# Movie Details
# ----------------------------------------

@login_required(login_url="login")
def movie_detail(request, id):

    movie = get_object_or_404(Movie, id=id)

    try:
        recommendations = recommend(movie.id)
    except Exception:
        recommendations = []

    in_wishlist = Wishlist.objects.filter(
        user=request.user,
        movie=movie
    ).exists()

    return render(request, "movie_detail.html", {
        "movie": movie,
        "recommendations": recommendations,
        "in_wishlist": in_wishlist,
    })


# ----------------------------------------
# Wishlist
# ----------------------------------------

@login_required(login_url="login")
def wishlist(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related("movie")

    return render(request, "wishlist.html", {
        "wishlist_items": wishlist_items
    })


# ----------------------------------------
# Add to Wishlist
# ----------------------------------------

@login_required(login_url="login")
def add_to_wishlist(request, id):

    movie = get_object_or_404(Movie, id=id)

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        movie=movie
    )

    if created:
        messages.success(request, f'"{movie.title}" added to your wishlist!')
    else:
        messages.info(request, f'"{movie.title}" is already in your wishlist.')

    return redirect("movie_detail", id=id)


# ----------------------------------------
# Remove from Wishlist
# ----------------------------------------

@login_required(login_url="login")
def remove_from_wishlist(request, id):

    movie = get_object_or_404(Movie, id=id)

    Wishlist.objects.filter(
        user=request.user,
        movie=movie
    ).delete()

    messages.success(request, f'"{movie.title}" removed from your wishlist.')

    return redirect("wishlist")