from django.urls import path
from . import views

urlpatterns = [
    # Home
    path("home/", views.home, name="home"),

    # Movie Details
    path("movie/<int:id>/", views.movie_detail, name="movie_detail"),

    # Wishlist
    path("wishlist/", views.wishlist, name="wishlist"),

    # Add to Wishlist
    path(
        "wishlist/add/<int:id>/",
        views.add_to_wishlist,
        name="add_to_wishlist",
    ),

    # Remove from Wishlist
    path(
        "wishlist/remove/<int:id>/",
        views.remove_from_wishlist,
        name="remove_from_wishlist",
    ),
]