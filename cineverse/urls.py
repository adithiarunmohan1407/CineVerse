from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from movies.views import landing

urlpatterns = [
    path("admin/", admin.site.urls),

    # Landing page
    path("", landing, name="landing"),

    # User Authentication
    path("", include("users.urls")),

    # Movie URLs
    path("", include("movies.urls")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)