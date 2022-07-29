from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters


from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Categories, Genre, Titles
from .serializers import (CategoriesSerializer,
                          GenreSerializer,
                          TitlesSerializer,
                          TitlesPostSerializer)
from .mixins import ListCreateDestroyViewSet
from users.permissions import IsAdmin, IsAdminOrReadOnly


class CategoriesViewSet(ListCreateDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ('name',)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', 'slug',)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'genre__slug', 'category__slug', 'year',  'name',
    )
    search_fields = ('genre__slug', 'category__slug', 'year',  'name',)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitlesSerializer
        return TitlesPostSerializer
