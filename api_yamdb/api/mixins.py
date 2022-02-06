from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Вьюсет для обработки запросов GET, POST и DELETE."""
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pass
