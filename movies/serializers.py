from rest_framework import serializers

from .models import Genre
from .models import Movie


class GenreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Genre
        fields = (
            'id',
            'name'
        )


class MovieSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Movie
        fields = (
            'id',
            'name',
            'year',
            'genres'
        )

    def __init__(self, *args, **kwargs):
        self.have_sequels = kwargs.pop('have_sequels', None)
        super(MovieSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        result = super(MovieSerializer, self).to_representation(obj)

        # Add the ``number_of_sequels`` field to the response object if the
        # object has any sequels.
        if self.have_sequels and obj.name in self.have_sequels:
            result['number_of_sequels'] = self.have_sequels[obj.name]

        return result
