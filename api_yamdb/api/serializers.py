from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Titles, Genre, Categories


class TitlesSerializer(serializers.ModelSerializer):
    """Сериалтзатор для модели Titles."""
    
    class Meta:
        fields = ('id', 'name', 'categories', 'genre', 'description', 'year')
        model = Titles


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""
    pass    
    

class CategoriesSerializer(serializers.ModelSerializer):
    """Сериалтзатор для модели Categories."""

#поле slug должно быть уникальным    
    
    class Meta:
        fields = ('name', 'slug',)
        model = Categories