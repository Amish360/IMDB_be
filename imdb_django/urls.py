from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


urlpatterns = [
    # Your other URL patterns

    path('api/', include([
        path("names/", views.NameListView.as_view(), name="name-list-create"),
        path("titles/", views.TitleList.as_view(), name="title-list"),
        path("search_names/", views.search_names, name="search_names"),
        path("search_movies/", views.search_movies, name="search_movies"),
        path("random_titles/", views.RandomTitleList.as_view(), name="search_movies"),
        path("api/create_favorite_tv_show/", views.create_user_favorite_tvshow, name="create_favorite_tv_show"),
    ]))

]
