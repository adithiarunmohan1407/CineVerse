from django.contrib import admin
from django.urls import path, include

from movies.views import landing

urlpatterns = [

    path("admin/", admin.site.urls),

    path("", landing, name="landing"),

    path("", include("users.urls")),

    path("", include("movies.urls")),

]