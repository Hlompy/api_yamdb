from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (CategorySerializer,
                             GenreSerializer,
                             TitleGetSerializer,
                             TitlePostSerializer)
from reviews.models import Category, Genre, Title


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Вьюсет для обработки запросов GET, POST и DELETE."""
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    """Управление категориями произведений."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListCreateDestroyViewSet):
    """Управление категориями жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Управление произведениями."""
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug')

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitlePostSerializer
        return TitleGetSerializer
