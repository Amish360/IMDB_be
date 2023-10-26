import random

from django.http import JsonResponse

import django_filters
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


from .models import *
from .pagination import TitlePagination
from .serializers import *



class TitleFilter(django_filters.FilterSet):
    class Meta:
        model = Title
        fields = {
            "title_Type": ["exact", "icontains"],
            "is_Adult": ["exact"],
            "genres__name": ["exact"],
        }


class TitleList(generics.ListAPIView):

    serializer_class = TitleSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = "__all__"  # Allow sorting on all fields
    filterset_fields = ["title_Type", "is_Adult"]  # Allow filtering on specific fields

    def get_queryset(self):

        queryset = Title.objects.filter(
            Q(title_Type__icontains="movie") | Q(title_Type__icontains="tvSeries")
        )


        return queryset




class NameListView(generics.ListAPIView):
    queryset = Name.objects.filter(
        Q(primary_Profession__icontains="actor")
        | Q(primary_Profession__icontains="actress")
    )
    serializer_class = NameSerializer


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


@api_view(["GET"])
def detail_movies(request):
    ID = request.GET.get("ID", "")

    # Query to filter based on the primaryName field in the Name model
    if ID:
        movies = Title.objects.filter(t_const__icontains=ID)
    else:
        movies = Title.objects.all()

    # Serialize the names using the serializer
    serializer = TitleSerializer(movies, many=True)

    return Response({"results": serializer.data})


@api_view(["GET"])
def detail_cast(request):
    ID = request.GET.get("ID", "")

    # Query to filter based on the primaryName field in the Name model
    if ID:
        cast = Name.objects.filter(n_const__icontains=ID)
    else:
        cast = Name.objects.all()

    # Serialize the names using the serializer
    serializer = NameSerializer(cast, many=True)

    return Response({"results": serializer.data})



@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request):
    t_const = request.data.get('t_const')

    if request.method == 'POST':
        # Add to wishlist
        item, created = WishlistItem.objects.get_or_create(user=request.user, tconst=t_const)
        return Response({'message': 'Added to wishlist'}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # Remove from wishlist
        WishlistItem.objects.filter(user=request.user, tconst=t_const).delete()
        return Response({'message': 'Removed from wishlist'}, status=status.HTTP_204_NO_CONTENT)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wishlist(request):
    # Retrieve the user's wishlist based on their user ID
    wishlist = WishlistItem.objects.filter(user=request.user)

    # Serialize the wishlist data as needed (e.g., using Django REST framework serializers)
    # You can also format the data as a JSON response
    wishlist_data = [{'tconst': item.tconst} for item in wishlist]

    return Response(wishlist_data, status=status.HTTP_200_OK)
