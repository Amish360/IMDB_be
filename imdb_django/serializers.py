from rest_framework import serializers

from .models import Genre, Name, Title, UserFavoriteTVShow


class UserFavoriteTVShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoriteTVShow
        fields = "__all__"


class NameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Name
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class TitleSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)  # Include the related genres

    class Meta:
        model = Title
        fields = "__all__"
