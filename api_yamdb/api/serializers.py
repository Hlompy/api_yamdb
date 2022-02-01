from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории произведения."""
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор категории жанра."""
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведения."""
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name')
    genre = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name')

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category', 'genre')
