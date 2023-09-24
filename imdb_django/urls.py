from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"userfavoritetvshows", views.UserFavoriteTVShowViewSet)

urlpatterns = [
    # Your other URL patterns
    path("shows/", include(router.urls)),
    path(
        "api/create_favorite_tvshow/",
        views.create_user_favorite_tvshow,
        name="create_favorite_tvshow",
    ),
    path(
        "api/random-titles/", views.RandomTitleList.as_view(), name="random-title-list"
    ),
    path("api/names/", views.NameListView.as_view(), name="name-list-create"),
    path("api/titles/", views.TitleList.as_view(), name="title-list"),
    path("api/search_names/", views.search_names, name="search_names"),
    path("api/search_movies/", views.search_movies, name="search_movies"),
]
