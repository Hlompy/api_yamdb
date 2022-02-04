from django.shortcuts import get_object_or_404, render
from rest_framework import mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Category, Genre, Review, Title

from api.permissions import IsAdminPermission, IsAuthorOrReadOnlyPermission
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

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


class GenreViewSet(ListCreateDestroyViewSet):
    """Управление категориями жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
