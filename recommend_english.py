import pandas as pd
import requests
from decouple import config
import scipy.sparse as sp
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_data():
    movie_data = pd.read_csv('./datasets/english_movies.csv')
    movie_data['title'] = movie_data['title'].str.lower()
    return movie_data


def combine_data(data):
    data_recommend = data.drop(columns=['tmdb_id', 'title', 'description'])
    data_recommend['combine'] = data_recommend[data_recommend.columns[0:4]].apply(
        lambda x: ','.join(x.dropna().astype(str)), axis=1)
    data_recommend = data_recommend.drop(
        columns=['director', 'cast', 'genres', 'keywords'])
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

    indices = pd.Series(data.index, index=data['title'])
    index = indices[title]

    sim_scores = list(enumerate(transform[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]

    movie_indices = [i[0] for i in sim_scores]

    movie_id = data['tmdb_id'].iloc[movie_indices]
    movie_title = data['title'].iloc[movie_indices]
    movie_genres = data['genres'].iloc[movie_indices]

    recommendation_data = pd.DataFrame(columns=['movie_id', 'title', 'genres'])

    recommendation_data['movie_id'] = movie_id
    recommendation_data['title'] = movie_title
    recommendation_data['genres'] = movie_genres

    return recommendation_data


def get_movie_image(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, config('API_KEY')))
    data_dict = response.json()
    return 'https://image.tmdb.org/t/p/original'+data_dict['poster_path']


def results(movie_name):
    movie_name = movie_name.lower()

    movie_df = get_data()
    combine_result = combine_data(movie_df)
    transform_result = transform_data(combine_result, movie_df)

    if movie_name not in movie_df['title'].unique():
        return 'NA'

    else:
        recommendations = recommend_movies(
            movie_name, movie_df, combine_result, transform_result)
        df = pd.DataFrame(recommendations.to_dict('records'))
        df['movie_image'] = df['movie_id'].apply(lambda x: get_movie_image(x))
        return df.to_dict(orient='records')
