from enum import Enum 

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

    def getAverageRating(self,movie):
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
            rating = self._movieRatings.getAverageRating(movie)
            if rating > best_rating:
                best_movie = movie 
                best_rating = rating      
        return best_movie.getTitle() if best_movie else None 
    
    def _recommendMovieExistingUser(self, user):
        best_movie = None 
        similarity_score = float('inf')

        for reviewer in self._movieRatings.getUsers():
            if reviewer.getId() == user.getId():
                continue
            score = self._getSimilarityScore(user, reviewer)
            if score < similarity_score:
                similarity_score = score
                recommended_movie = self._recommendUnwatchedMovie(user,reviewer)
                best_movie = recommended_movie if recommended_movie else best_movie
        return best_movie.getTitle() if best_movie else None 

    def _getSimilarityScore(self, user1, user2):
        user1_id = user1.getId()
        user2_id = user2.getId()
        user2_movies = self._movieRatings.getUserMovies(user2)
        score = float('inf') # Lower is better

        for movie in user2_movies:
            cur_movie_ratings = self._movieRatings.getMovieRatings(movie)
            if user1_id in cur_movie_ratings:
                score = 0 if score == float('inf') else score
                score += abs(cur_movie_ratings[user1_id].value - cur_movie_ratings[user2_id].value)
        return score

    def _recommendUnwatchedMovie(self, user, reviewer):
        user_id = user.getId()
        reviewer_id = reviewer.getId()
        best_movie = None
        best_rating = 0

        reviewer_movies = self._movieRatings.getUserMovies(reviewer)
        for movie in reviewer_movies:
            cur_movie_ratings = self._movieRatings.getMovieRatings(movie)
            if user_id not in cur_movie_ratings and cur_movie_ratings[reviewer_id].value > best_rating:
                best_movie = movie
                best_rating = cur_movie_ratings[reviewer_id].value
        return best_movie

user1 = User(1, 'User 1')
user2 = User(2, 'User 2')
user3 = User(3, 'User 3')

movie1 = Movie(1, 'Batman Begins')
movie2 = Movie(2, 'Liar Liar')
movie3 = Movie(3, 'The Godfather')

ratings = RatingRegister()
ratings.addRating(user1, movie1, MovieRating.FIVE)
ratings.addRating(user1, movie2, MovieRating.TWO)
ratings.addRating(user2, movie2, MovieRating.TWO)
ratings.addRating(user2, movie3, MovieRating.FOUR)

recommender = MovieRecommendation(ratings)

print(recommender.recommendMovie(user1)) # The Godfather
print(recommender.recommendMovie(user2)) # Batman Begins
print(recommender.recommendMovie(user3)) # Batman Begins