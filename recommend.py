from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse as sp
import ast
import pandas as pd
import requests
from decouple import config
import imdb
ia = imdb.IMDb()


def get_data():
    movie_data = pd.read_csv('all_movies_data.csv')
    movie_data['name'] = movie_data['name'].str.lower()
    return movie_data


def combine_data(data):
    data_recommend = data.drop(
        columns=['tmdb_id', 'imdb_id', 'name', 'description', 'year', 'rating'], axis=1)
    data_recommend['combine'] = data_recommend[data_recommend.columns[0:4]].apply(
        lambda x: ','.join(x.dropna().astype(str)), axis=1)
    data_recommend = data_recommend.drop(
        columns=['directors', 'cast', 'genres'])
    return data_recommend


def transform_data(data_combine, data):
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(data_combine['combine'])

    tfidf = TfidfVectorizer(stop_words='english',
                            token_pattern=u'([a-zA-Z-/]{1,})')
    tfidf_matrix = tfidf.fit_transform(data['description'])

    combine_sparse = sp.hstack([count_matrix, tfidf_matrix], format='csr')

    cosine_sim = cosine_similarity(combine_sparse, combine_sparse)

    return cosine_sim


def recommend_movies(title, data, combine, transform):

    indices = pd.Series(data.index, index=data['suggestions'])
    index = indices[title]

    sim_scores = list(enumerate(transform[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:13]

    movie_indices = [i[0] for i in sim_scores]

    imdb_id = data['imdb_id'].iloc[movie_indices]
    tmdb_id = data['tmdb_id'].iloc[movie_indices]
    movie_year = data['year'].iloc[movie_indices]
    movie_title = data['name'].iloc[movie_indices]
    movie_genres = data['genres'].iloc[movie_indices]

    recommendation_data = pd.DataFrame(
        columns=['imdb_id', 'tmdb_id', 'year', 'title', 'genres'])

    recommendation_data['imdb_id'] = imdb_id
    recommendation_data['tmdb_id'] = tmdb_id
    recommendation_data['year'] = movie_year
    recommendation_data['title'] = movie_title
    recommendation_data['genres'] = movie_genres

    return recommendation_data


def get_poster(id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key={}'.format(id, config('API_KEY')))
    data_dict = response.json()
    return 'https://image.tmdb.org/t/p/original'+data_dict['poster_path']


def results(movie_name):
    movie_df = get_data()
    movie_df = movie_df.assign(
        suggestions=movie_df.name+' ('+movie_df['year'].astype(str)+')')
    combine_result = combine_data(movie_df)
    transform_result = transform_data(combine_result, movie_df)

    recommendations = recommend_movies(
        movie_name, movie_df, combine_result, transform_result)
    df = pd.DataFrame(recommendations.to_dict('records'))
    df['poster'] = df['tmdb_id'].apply(lambda x: get_poster(x))
    return df.to_dict(orient='records')
