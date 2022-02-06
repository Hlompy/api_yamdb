from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.mixins import ListCreateDestroyViewSet
from api.permissions import (
    IsAdminOrReadOnlyPermission, IsAdminPermission, IsAuthorOrAdminOrModerator,
)
from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer, ReviewSerializer,
    TitleGetSerializer, TitlePostSerializer,
)
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(ListCreateDestroyViewSet):
    """Управление категориями произведений."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = []
        else:
            self.permission_classes = [IsAdminPermission, ]
        return super(CategoryViewSet, self).get_permissions()


class GenreViewSet(ListCreateDestroyViewSet):
    """Управление категориями жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = []
        else:
            self.permission_classes = [IsAdminPermission, ]
        return super(GenreViewSet, self).get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    """Управление произведениями."""
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year',)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitlePostSerializer
        return TitleGetSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = []
        else:
            self.permission_classes = [IsAdminPermission, ]
        return super(TitleViewSet, self).get_permissions()

    def get_queryset(self):
        queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
        genre = self.request.query_params.get('genre')
        category = self.request.query_params.get('category')
        name = self.request.query_params.get('name')
        if genre:
            queryset = queryset.filter(genre__slug=genre)
        if category:
            queryset = queryset.filter(category__slug=category)
        if name:
            queryset = queryset.filter(name__contains=name)
        return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    """Работа с отзывами."""
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModerator
    )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Работа с комментариями."""
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModerator
    )

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(
            author=self.request.user,
            review_id=self.kwargs.get('review_id')
        )
