from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("movie/<int:id>/", views.movie_detail, name="movie_detail"),

    path("wishlist/", views.wishlist, name="wishlist"),

    path(
        "wishlist/add/<int:id>/",
        views.add_to_wishlist,
        name="add_to_wishlist"
    ),

    path(
        "wishlist/remove/<int:id>/",
        views.remove_from_wishlist,
        name="remove_from_wishlist"
    ),
]