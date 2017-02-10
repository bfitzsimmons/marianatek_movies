from __future__ import unicode_literals

import re

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Genre(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Movie(models.Model):
    name = models.CharField(max_length=128)
    year = models.DateField()
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'year')

    @classmethod
    def have_sequels(self):
        """Return an object containing movies that have sequels. Included in
        the data is a sequel count for each movie.

        """
        # Get any movies that may be a sequel to another movie in the db.
        regex = ' (VIII|VII|VI|V|IV|III|II)?$'
        sequels = Movie.objects.filter(name__regex=regex)

        # For each potential sequel, find the original version of the movie and
        # add it to the result set -- with its corresponding sequel count.
        results = {}
        for sequel in sequels:
            # Get the original name.
            prefix = re.sub(regex, '', sequel.name)

            # Get the original movie from the db -- if it exists.
            movies = Movie.objects.filter(
                name=prefix,
                genres=sequel.genres.all()
            )

            # Jump to the next loop if the sequel has no original in the db.
            if len(movies) < 1:
                continue

            # Add the movie and count to the results.
            if movies[0].name not in results:
                results[movies[0].name] = 1
            else:
                results[movies[0].name] += 1

        return results
