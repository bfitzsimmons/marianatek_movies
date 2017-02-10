import os.path
import csv

from django.core.management.base import BaseCommand, CommandError

from movies.models import Genre
from movies.models import Movie


class Command(BaseCommand):
    help = 'Imports the Movie data from the tsv file'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str)

    def handle(self, *args, **options):
        filepath = options['filepath']

        # Check for the existence of the import data file.
        if not os.path.isfile(filepath):
            raise CommandError('file "{}" does not exist'.format(filepath))

        # Open the tsv file and get that data.
        with open(filepath) as tsvin:
            tsvin = csv.reader(tsvin, delimiter='\t')

            for line in tsvin:
                movie_name = line[0]
                movie_year = line[1]
                genre_name = line[2]

                # Deal with the genres.
                genre, created = Genre.objects.get_or_create(name=genre_name)
                if created:
                    self.stdout.write('Genre "{}" created'.format(genre_name))

                # Deal with the movies.
                movie, created = Movie.objects.get_or_create(
                    name=movie_name,
                    year='{}-01-01'.format(movie_year)
                )
                movie.genres.add(genre)
                if created:
                    action = 'created'
                else:
                    action = 'updated'
                self.stdout.write('Movie "{0}" {1}'.format(movie_name, action))

        self.stdout.write('The movies have been successfully imported')
