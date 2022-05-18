import pandas as pd
from scipy import sparse

ratings = pd.read_csv('all_ratings.csv')
movies = pd.read_csv('all_movies.csv')
ratings = pd.merge(movies, ratings).drop(['genres', 'timestamp'], axis=1)

userRatings = ratings.pivot_table(index=['userId'], columns=[
                                  'title'], values='rating')
userRatings = userRatings.dropna(thresh=10, axis=1).fillna(0, axis=1)

corrMatrix = userRatings.corr(method='pearson')


def get_similar_movies(movie_name, rating):
    similar_ratings = corrMatrix[movie_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings


def get_recommendations(ratings_list):
    similar_movies = pd.DataFrame()
    for movie, rating in ratings_list:
        similar_movies = similar_movies.append(
            get_similar_movies(movie, rating), ignore_index=True)
    ans = similar_movies.sum().sort_values(ascending=False).head(12)
    return ans.index.values
