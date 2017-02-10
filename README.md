# Mariana Tek Movies

## Setup
1. Check out the code: `git clone git@github.com:bfitzsimmons/marianatek_movies.git
`
1. Create a virtualenv: `cd marianatek_movies/ && virtualenv venv && source venv/bin/activate`
1. Install requirements: `pip install -r requirements.txt`
1. Run the migrations: `python manage.py migrate`
1. Run the tests: `python manage.py test`

## Import Movie Data
Import the movie data from the tsv: `python manage.py import data/movies_genres.tsv`

## Test out the API
Please start the dev. server (`python manage.py runserver`) before running any of the following commands.

**All URL's may be retrieved using a web browser. All `curl` commands should be run from a command prompt.**

### Genres
* Get list of genres: http://localhost:8000/api/genres/
* Add a new genre: `curl -X POST -H "Content-Type: application/json" -d '{"name": "Science Fiction"}' "http://localhost:8000/api/genres/"`
* Get the newly added genre: http://localhost:8000/api/genres/24/
* Modify the newly added genre: `curl -X PUT -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{"name": "SciFy"}' "http://localhost:8000/api/genres/24/"`
* Delete the newly added genre: `curl -X DELETE -H "Cache-Control: no-cache" "http://localhost:8000/api/genres/24/"`
* Get the movie counts per genre: http://localhost:8000/api/genres/movie-counts/
* Get the movie count for a single genre: http://localhost:8000/api/genres/9/movie-count/
* Get the year/genre combination with the most movies: http://localhost:8000/api/genres/most-movies-per-year/

### Movies
* Get a list of movies: http://localhost:8000/api/movies/
* Add a new movie: `curl -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{"name": "Big Her0 6",	"year": "2014-01-01",	"genres": ["http://localhost:8000/api/genres/4/"]}' "http://localhost:8000/api/movies/"`
* Get the newly added movie: http://localhost:8000/api/movies/7149/
* Modify the newly added movie: `curl -X PUT -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{"name": "Big Hero 6", "year": "2014-01-01",	"genres": ["http://localhost:8000/api/genres/4/"]}' "http://localhost:8000/api/movies/7149/"`
* Delete the newly added movie: `curl -X DELETE -H "Cache-Control: no-cache" "http://localhost:8000/api/movies/7149/"`
* Get movies by genre: http://localhost:8000/api/movies/?genre=drama
* Show the sequels related field (`number_of_sequels`) when getting a list of movies (see record 1556): http://localhost:8000/api/movies/?limit=50&offset=1550&sequels=True
