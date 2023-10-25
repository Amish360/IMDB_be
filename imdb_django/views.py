import random

import django_filters
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Genre, Name, Title, UserFavoriteTVShow
from .pagination import TitlePagination
from .serializers import (
    GenreSerializer,
    NameSerializer,
    TitleSerializer,
    UserFavoriteTVShowSerializer,
)


class TitleFilter(django_filters.FilterSet):
    class Meta:
        model = Title
        fields = {
            "title_Type": ["exact", "icontains"],
            "is_Adult": ["exact"],
            "genres__name": ["exact"],
        }


class TitleList(generics.ListAPIView):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = "__all__"  # Allow sorting on all fields
    filterset_fields = ["titleType", "isAdult"]  # Allow filtering on specific fields

    def get_queryset(self):
        queryset = Title.objects.filter(
            Q(title_Type__icontains="movie") | Q(title_Type__icontains="tvSeries")
        )

        return queryset


class UserFavoriteTVShowViewSet(viewsets.ModelViewSet):
    queryset = UserFavoriteTVShow.objects.all()
    serializer_class = UserFavoriteTVShowSerializer


class NameListView(generics.ListAPIView):
    queryset = Name.objects.filter(
        Q(primary_Profession__icontains="actor")
        | Q(primary_Profession__icontains="actress")
    )
    serializer_class = NameSerializer


@api_view(["POST"])
def create_user_favorite_tvshow(request):
    if request.method == "POST":
        serializer = UserFavoriteTVShowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RandomTitleList(APIView):
    def get(self, request):
        # Get 5 random TV shows
        random_titles = random.sample(
            list(
                Title.objects.filter(
                    Q(title_Type__icontains="movie") | Q(title_Type__icontains="tvSeries")
                )
            ),
            5,
        )

        # Serialize the titles
        serializer = TitleSerializer(random_titles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def search_names(request):
    search_term = request.GET.get("search", "")

    # Query to filter based on the primaryName field in the Name model
    if search_term:
        names = Name.objects.filter(primary_Name__icontains=search_term).order_by('primary_Name')
    else:
        names = Name.objects.all().order_by('primary_Name')

    # Serialize the names using the serializer
    serializer = NameSerializer(names, many=True)

    return Response({"results": serializer.data})


@api_view(["GET"])
def search_movies(request):
    search_term = request.GET.get("search", "")

    # Query to filter based on the primaryTitle field in the Title model
    if search_term:
        movies = Title.objects.filter(primary_Title__icontains=search_term).order_by('primary_Title')
    else:
        movies = Title.objects.all().order_by('primary_Title')

    # Serialize the movies using the serializer
    serializer = TitleSerializer(movies, many=True)

    return Response({"results": serializer.data})
