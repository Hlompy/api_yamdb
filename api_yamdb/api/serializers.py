import datetime as dt
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории произведения."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор категории жанра."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор вывода информации о произведениях."""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitlePostSerializer(serializers.ModelSerializer):
    """Сериализатор записи информации о произведениях."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug',
    )

    class Meta:
        model = Title
        fields = '__all__'
        # extra_qwargs = {'description': {'required': False}}
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=['name', 'year', 'category'],
                message='Такое произведение уже есть в базе'
            )
        ]

    def validate_year(self, value):
        """Проверка, что год выпуска не привышает текущий."""
        if value > dt.date.today().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего'
            )
        return value
