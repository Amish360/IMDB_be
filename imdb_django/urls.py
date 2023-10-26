from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

urlpatterns = [
    # Your other URL patterns
    path("shows/", include(router.urls)),
    path('api/', include([
        path("names/", views.NameListView.as_view(), name="name-list-create"),
        path("titles/", views.TitleList.as_view(), name="title-list"),
        path("search_names/", views.search_names, name="search_names"),
        path("search_movies/", views.search_movies, name="search_movies"),
        path("detail_movies/", views.detail_movies, name="detail_movies"),
        path("detail_cast/", views.detail_cast, name="detail_cast"),
        path("wishlist/", views.add_to_wishlist, name="add_to_wishlist"),
        path("get_wishlist/", views.get_wishlist, name="get_wishlist"),
    ]))

]
