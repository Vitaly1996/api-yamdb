from reviews.models import Titles, Genre, Categories
from rest_framework import serializers
from django.db.models import Avg
import datetime as dt


class TitlesPostSerializer(serializers.ModelSerializer):
    "Cериализатор для модели Titles для записи данных"
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    class Meta:
        model = Titles
        fields = (
           'id', 'name', 'year', 'description', 'genre', 'category',
        )


class GenreSerializer(serializers.ModelSerializer):
    "Cериализатор для модели Genre"
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategoriesSerializer(serializers.ModelSerializer):
    "Cериализатор для модели Categories"

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    "Сериализотор для модели Titles для чтения данных"
    genre = GenreSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    # rating = serializers.IntegerField(
    #     Titles.objects.annotate(rating=Avg('reviews__score'))
    # )

    class Meta:
        model = Titles

        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating'
        )

        def validate_year(self, value):
            year = dt.date.today().year
            if not value <= year:
                raise serializers.ValidationError(
                    'Проверьте год издания произведения!')
            return value
