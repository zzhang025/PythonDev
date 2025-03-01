class Movie:
    def __init__(self, id, title):
        self._id = id
        self._title = title

    def getId(self):
        return self._id

    def getTitle(self):
        return self._title


class User:
    def __init__(self, id, name) -> None:
        self._id = id
        self._name = name

    def getId(self):
        return self._id


from enum import Enum


class MovieRating(Enum):
    NOT_RATED = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class RatingRegister:
    def __init__(self) -> None:
        self._userMovies = {}
        self._movieRatings = {}

        self._movies = []
        self._users = []

    def addRating(self, user, movie, rating):
        if movie.getId() not in self._movieRatings:
            self._movieRatings[movie.getId()] = {}
            self._movies.append(movie)

        if user.getId() not in self._userMovies:
            self._userMovies[user.getId()] = []
            self._users.append(user)

        self._userMovies[user.getId()].append(movie)
        self._movieRatings[movie.getId()][user.getId()] = rating

    def getAverageRating(self, movie):
        if movie.getId() not in self._movieRatings:
            return MovieRating.NOT_RATED.value
        ratings = self._movieRatings[movie.getId()].values()
        ratingsValues = [rating.value for rating in ratings]
        return sum(ratingsValues) / len(ratingsValues)

    def getUsers(self):
        return self._users

    def getMovies(self):
        return self._movies

    def getUserMovies(self, user):
        return self._userMovies.get(user.getId(), [])

    def getMovieRatings(self, movie):
        return self._movieRatings.get(movie.getId(), {})


class MovieRecommendation:
    def __init__(self, ratings) -> None:
        self._movieRatings = ratings

    def recommendMovie(self, user):
        if len(self._movieRatings.getUserMovies(user)) == 0:
            return self._recommendMovieNewUser()
        else:
            return self._recommendMovieExistingUser(user)

    def _recommendMovieNewUser(self):
        best_movie = None
        best_rating = 0
        for movie in self._movieRatings.getMovies():
            rating = self._movieRatings.getAverageRating(Movie)
            if rating > best_rating:
                best_movie = movie
                best_rating = rating

        return best_movie.getTitle() if best_movie else None
