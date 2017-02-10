from rest_framework.filters import BaseFilterBackend


class MovieFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        # Get the ``genre`` query param. from the URL.
        genre = request.query_params.get('genre', None)

        # Filter the queryset.
        if genre:
            queryset = queryset.filter(genres__name__iexact=genre)

        return queryset
