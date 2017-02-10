from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from rest_framework.decorators import detail_route
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet

from .filters import MovieFilter
from .models import Genre
from .models import Movie
from .serializers import GenreSerializer
from .serializers import MovieSerializer


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    @list_route(url_path='movie-counts')
    def movie_counts(self, request):
        """Return a list of genres with a count indicating the number of movies
        of that genre.

        """
        genres = (
            Genre.objects
            .annotate(count=Count('movie'))
            .order_by('-count')
        )

        counts = []
        for genre in genres:
            counts.append({
                'genre_url': reverse(
                    'genre-detail', args=(genre.id,), request=request
                ),
                'count': genre.count
            })

        return Response(counts)

    @detail_route(url_path='movie-count')
    def movie_count(self, request, pk):
        """Return an object containing a reference to the requested genre, as
        well as a count indicating the number of movies of that genre.

        """
        try:
            genre = Genre.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({})

        return Response({
            'genre_url': reverse(
                'genre-detail', args=(genre.id,), request=request
            ),
            'count': Movie.objects.filter(genres=genre).count()
        })

    @list_route(url_path='most-movies-per-year')
    def most_movies_per_year(self, request):
        """Return an object containing data on the year and genre with the most
        movies.

        """
        try:
            genre = (
                Genre.objects.values('name', 'movie__year')
                .annotate(count=Count('movie', distinct=True))
                .order_by('-count')[0]
            )
        except IndexError:
            return Response({})

        return Response({
            'genre': genre['name'],
            'year': genre['movie__year'].strftime('%Y'),
            'count': genre['count']
        })


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.prefetch_related('genres').all().order_by('name')
    serializer_class = MovieSerializer
    filter_backends = (MovieFilter,)

    def __init__(self, *args, **kwargs):
        self.have_sequels = None

    def list(self, request):
        # Do we need to find sequels?
        if 'sequels' in request.query_params:
            self.have_sequels = Movie.have_sequels()

        # Filter the queryset.
        queryset = self.filter_queryset(self.get_queryset())

        # Pagination the queryset.
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True,
                have_sequels=self.have_sequels
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset,
            many=True,
            have_sequels=self.have_sequels
        )
        return Response(serializer.data)
