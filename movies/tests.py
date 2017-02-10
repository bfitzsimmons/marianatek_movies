# from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.test import APITestCase


class GenreViewSetTests(APITestCase):

    def test_genre_creation(self):
        # Create the genre record.
        data = {'name': 'Drama'}
        response = self.client.post('/api/genres/', data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_genre_modification(self):
        # Create the genre record.
        data = {'name': 'Dramaa'}
        response = self.client.post('/api/genres/', data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Update the genre record.
        url = '/api/genres/{}/'.format(response.data['id'])
        data = {'name': 'Drama'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Drama')

    def test_genre_deletion(self):
        # Create the genre record.
        data = {'name': 'Drama'}
        response = self.client.post('/api/genres/', data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Delete the genre record.
        url = '/api/genres/{}/'.format(response.data['id'])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def test_genre_detail(self):
        # Create the genre record.
        data = {'name': 'Drama'}
        response = self.client.post('/api/genres/', data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Get the genre record.
        url = '/api/genres/{}/'.format(response.data['id'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Drama')

    def test_genre_list(self):
        # Create the genre records.
        data = {'name': 'Drama'}
        response = self.client.post('/api/genres/', data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        data = {'name': 'Family'}
        response = self.client.post('/api/genres/', data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Get the genre records.
        response = self.client.get('/api/genres/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['name'], 'Drama')
        self.assertEqual(response.data['results'][1]['name'], 'Family')


class GenreViewSetMethodTests(APITestCase):

    def setUp(self):
        # Create the genre records.
        data = [
            {'name': 'Comedy'},
            {'name': 'Family'},
            {'name': 'Drama'}
        ]
        self.genre_data = []
        for item in data:
            response = self.client.post('/api/genres/', item, format='json')
            self.genre_data.append({
                'data': response.data,
                'url': '/api/genres/{}/'.format(response.data['id'])
            })

        # Create the movie records.
        data = [
            {
                'name': 'A Brew Hope',
                'year': '2012-01-01',
                'genres': [self.genre_data[0]['url']]
            },
            {
                'name': 'A Brew Hope II',
                'year': '2013-01-01',
                'genres': [self.genre_data[0]['url']]
            },
            {
                'name': 'A Brew Hope III',
                'year': '2014-01-01',
                'genres': [self.genre_data[0]['url']]
            },
            {
                'name': 'Big Hero 6',
                'year': '2014-01-01',
                'genres': [self.genre_data[1]['url']]
            }
        ]
        self.movie_data = []
        for item in data:
            response = self.client.post('/api/movies/', item, format='json')
            self.movie_data.append(response.data)

    def test_movie_counts(self):
        response = self.client.get('/api/genres/movie-counts/')
        self.assertEqual(response.data[0]['count'], 3)
        self.assertEqual(
            response.data[0]['genre_url'],
            'http://testserver{}'.format(self.genre_data[0]['url'])
        )
        self.assertEqual(response.data[1]['count'], 1)
        self.assertEqual(
            response.data[1]['genre_url'],
            'http://testserver{}'.format(self.genre_data[1]['url'])
        )

    def test_movie_count(self):
        url = '/api/genres/{}/movie-count/'.format(
            self.genre_data[0]['data']['id']
        )
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(
            response.data['genre_url'],
            'http://testserver{}'.format(self.genre_data[0]['url'])
        )

    def test_most_movies_per_year(self):
        # Modify the existing records so that more comedies occur in 2012.
        data = {'year': '2012-01-01'}
        for i in range(3):
            url = '/api/movies/{}/'.format(i + 1)
            response = self.client.patch(url, data, format='json')

        # Get the genre and year with the most movies.
        response = self.client.get('/api/genres/most-movies-per-year/')
        self.assertEqual(
            response.data['genre'],
            self.genre_data[0]['data']['name']
        )
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(response.data['year'], '2012')


class MovieViewSetSpecialTests(APITestCase):

    def setUp(self):
        # Create the genre records.
        data = [
            {'name': 'Comedy'},
            {'name': 'Family'},
            {'name': 'Drama'}
        ]
        self.genre_data = []
        for item in data:
            response = self.client.post('/api/genres/', item, format='json')
            self.genre_data.append({
                'data': response.data,
                'url': '/api/genres/{}/'.format(response.data['id'])
            })

        # Create the movie records.
        data = [
            {
                'name': 'A Brew Hope',
                'year': '2012-01-01',
                'genres': [self.genre_data[0]['url']]
            },
            {
                'name': 'A Brew Hope II',
                'year': '2013-01-01',
                'genres': [self.genre_data[0]['url']]
            },
            {
                'name': 'A Brew Hope III',
                'year': '2014-01-01',
                'genres': [self.genre_data[0]['url']]
            },
            {
                'name': 'Big Hero 6',
                'year': '2014-01-01',
                'genres': [self.genre_data[1]['url']]
            }
        ]
        self.movie_data = []
        for item in data:
            response = self.client.post('/api/movies/', item, format='json')
            self.movie_data.append(response.data)

    def test_sequel_count(self):
        response = self.client.get('/api/movies/?sequels=True')
        results = response.data['results']
        self.assertEqual(response.data['count'], 4)
        self.assertEqual(results[0]['name'], 'A Brew Hope')
        self.assertEqual(results[0]['year'], '2012-01-01')
        self.assertEqual(
            results[0]['genres'],
            ['http://testserver{}'.format(self.genre_data[0]['url'])]
        )
        self.assertTrue('number_of_sequels' in results[0])
        self.assertEqual(results[0]['number_of_sequels'], 2)

        self.assertEqual(results[1]['name'], 'A Brew Hope II')
        self.assertEqual(results[1]['year'], '2013-01-01')
        self.assertEqual(
            results[1]['genres'],
            ['http://testserver{}'.format(self.genre_data[0]['url'])]
        )
        self.assertTrue('number_of_sequels' not in results[1])

        self.assertEqual(results[2]['name'], 'A Brew Hope III')
        self.assertEqual(results[2]['year'], '2014-01-01')
        self.assertEqual(
            results[2]['genres'],
            ['http://testserver{}'.format(self.genre_data[0]['url'])]
        )
        self.assertTrue('number_of_sequels' not in results[2])

        self.assertEqual(results[3]['name'], 'Big Hero 6')
        self.assertEqual(results[3]['year'], '2014-01-01')
        self.assertEqual(
            results[3]['genres'],
            ['http://testserver{}'.format(self.genre_data[1]['url'])]
        )
        self.assertTrue('number_of_sequels' not in results[3])


class MovieViewSetTests(APITestCase):

    def setUp(self):
        # Create the genre records.
        data = {'name': 'Comedy'}
        response = self.client.post('/api/genres/', data, format='json')
        self.genre_url = '/api/genres/{}/'.format(response.data['id'])

    def test_movie_creation(self):
        # Create the movie record.
        data = {
            'name': 'A Brew Hope',
            'year': '2012-01-01',
            'genres': [self.genre_url]
        }
        response = self.client.post('/api/movies/', data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'A Brew Hope')
        self.assertEqual(response.data['year'], '2012-01-01')
        self.assertEqual(
            response.data['genres'],
            ['http://testserver{}'.format(self.genre_url)]
        )

    def test_movie_modification_put(self):
        # Create the movie record.
        data = {
            'name': 'A Brew Hopee',
            'year': '2012-01-01',
            'genres': [self.genre_url]
        }
        response = self.client.post('/api/movies/', data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Update the movie record (PUT).
        url = '/api/movies/{}/'.format(response.data['id'])
        data = {
            'name': 'A Brew Hope',
            'year': '2012-01-01',
            'genres': [self.genre_url]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['name'], 'A Brew Hope')
        self.assertEqual(response.data['year'], '2012-01-01')
        self.assertEqual(
            response.data['genres'],
            ['http://testserver{}'.format(self.genre_url)]
        )

    def test_movie_modification_patch(self):
        # Create the movie record.
        data = {
            'name': 'A Brew Hopee',
            'year': '2012-01-01',
            'genres': [self.genre_url]
        }
        response = self.client.post('/api/movies/', data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Update the movie record (PATCH).
        url = '/api/movies/{}/'.format(response.data['id'])
        data = {
            'name': 'A Brew Hope'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['name'], 'A Brew Hope')
        self.assertEqual(response.data['year'], '2012-01-01')
        self.assertEqual(
            response.data['genres'],
            ['http://testserver{}'.format(self.genre_url)]
        )

    def test_movie_deletion(self):
        # Create the movie record.
        data = {
            'name': 'A Brew Hopee',
            'year': '2012-01-01',
            'genres': [self.genre_url]
        }
        response = self.client.post('/api/movies/', data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Delete the movie record.
        url = '/api/movies/{}/'.format(response.data['id'])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def test_movies_detail(self):
        # Create the movie record.
        data = {
            'name': 'A Brew Hope',
            'year': '2012-01-01',
            'genres': [self.genre_url]
        }
        response = self.client.post('/api/movies/', data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Get the movies record.
        url = '/api/movies/{}/'.format(response.data['id'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['name'], 'A Brew Hope')
        self.assertEqual(response.data['year'], '2012-01-01')
        self.assertEqual(
            response.data['genres'],
            ['http://testserver{}'.format(self.genre_url)]
        )

    def test_movie_list(self):
        # Create the movie record.
        data = {
            'name': 'A Brew Hope',
            'year': '2012-01-01',
            'genres': [self.genre_url]
        }
        response = self.client.post('/api/movies/', data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        data = {
            'name': 'A Brew Hope II',
            'year': '2013-01-01',
            'genres': [self.genre_url]
        }
        response = self.client.post('/api/movies/', data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Get the movie records.
        response = self.client.get('/api/movies/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['name'], 'A Brew Hope')
        self.assertEqual(response.data['results'][0]['year'], '2012-01-01')
        self.assertEqual(
            response.data['results'][0]['genres'],
            ['http://testserver{}'.format(self.genre_url)]
        )
        self.assertEqual(response.data['results'][1]['name'], 'A Brew Hope II')
        self.assertEqual(response.data['results'][1]['year'], '2013-01-01')
        self.assertEqual(
            response.data['results'][1]['genres'],
            ['http://testserver{}'.format(self.genre_url)]
        )
