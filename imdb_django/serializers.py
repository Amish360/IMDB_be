from rest_framework import serializers

from imdb_django.models import WishlistItem, Name, Genre, TitleAka, TitleCrew, TitlePrincipal, TitleRating, Title


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = "__all__"


class NameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Name
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class TitleAkaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleAka
        fields = "__all__"


from rest_framework import serializers

class TitleCrewRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `TitleCrew` related objects.
    """

    def to_representation(self, value):
        """
        Serialize related `TitleCrew` objects to a simple textual representation.
        """
        try:
            if isinstance(value, TitleCrew):
                # Modify this to match your model's field or fields
                representation = 'TitleCrew: Writers - ' + ', '.join(str(writer) for writer in value.writers.all()) + ', Directors - ' + ', '.join(str(director) for director in value.directors.all())
                return representation
        except Exception as e:
            print(f'Error in to_representation for TitleCrewRelatedField: {str(e)}')
            print(f'Value causing the error: {value}')
            raise



class TitleCrewSerializer(serializers.ModelSerializer):
    directors = TitleCrewRelatedField(many=True, read_only=True)
    writers = TitleCrewRelatedField(many=True, read_only=True)

    class Meta:
        model = TitleCrew
        fields = '__all__'


class TitlePrincipalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitlePrincipal
        fields = "__all__"


class TitleRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleRating
        fields = "__all__"


class TitleSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    rating = TitleRatingSerializer(read_only=True)
    crew = TitleCrewSerializer(many=True, read_only=True)
    principals = TitlePrincipalSerializer(read_only=True)

    class Meta:
        model = Title
        fields = "__all__"
