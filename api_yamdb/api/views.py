from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters


from reviews.models import Categories, Genre, Titles
from .serializers import (CategoriesSerializer,
                          GenreSerializer,
                          TitlesSerializer,
                          TitlesPostSerializer)
from .mixins import ListCreateDestroyViewSet
from users.permissions import IsAdmin, IsAdminOrReadOnly
from .filters import  TitlesFilter


class CategoriesViewSet(ListCreateDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = [IsAdminOrReadOnly]
    filter_class = TitlesFilter
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    filter_class = TitlesFilter
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (filters.SearchFilter,)
    filter_class = TitlesFilter
    search_fields = ('genre__slug', 'category__slug', 'year',  'name',)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitlesSerializer
        return TitlesPostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrReadOnly, ]

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAdminOrReadOnly, ]

    def get_queryset(self):
        review = get_object_or_404(Titles, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)







