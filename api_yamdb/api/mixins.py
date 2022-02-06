from rest_framework import mixins, viewsets


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Вьюсет для обработки запросов GET, POST и DELETE."""
    pass
