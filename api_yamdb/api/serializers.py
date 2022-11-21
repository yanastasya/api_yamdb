import datetime as dt

from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from reviews.models import Title, Genre, Categorie, Review, Comment


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class CategorieSerializer(serializers.ModelSerializer):
    """Сериалтзатор для модели Categorie."""
    class Meta:
        model = Categorie
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title.
    Для GET запросов к эндпоинтам /title/ и /title/id/.
    """

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorieSerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'category', 'genre', 'description', 'year', 'rating'
        )
        model = Title

    def get_rating(self, data):
        title = get_object_or_404(
            Title,
            id=data.id)
        avg = Review.objects.filter(title=title).aggregate(Avg('score'))
        return avg['score__avg']


class TitlePostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title.
    Для POST запросов к эндпоинтам /title/ и /title/id/.
    """
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categorie.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'category', 'genre', 'description', 'year')
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if not (value <= year):
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего.'
            )

        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['title', ]
