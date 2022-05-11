from flask import Flask, render_template, request, json
from flask_cors import CORS
import recommend
import pandas as pd
import pickle
from decouple import config
from bs4 import BeautifulSoup as soup
import urllib.request as reqs
import requests


df = pd.read_csv('all_movies_data.csv')
df = df.assign(suggestions=df.name+' ('+df['year'].astype(str)+')')


def get_sentiment(reviews):
    sentiments = []
    vectorizer = pickle.load(open('./sentiment-model/transform.pkl', 'rb'))
    arr = vectorizer.transform(reviews)
    clf = pickle.load(open('./sentiment-model/mnb.pkl', 'rb'))
    sentiments = clf.predict(arr)
    return sentiments


def get_movie_info(tmdb_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key={}'.format(tmdb_id, config('API_KEY')))
    return response.json()


def get_reviews_and_sentiment(imdb_id):
    sauce = reqs.urlopen(
        'https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdb_id)).read()

    page_soup = soup(sauce, 'lxml')
    results = page_soup.find_all("div", {"class": "text show-more__control"})
    reviews_list = []
    i = 0
    for review in results:
        reviews_list.append(review.text)
        i = i+1
        if i >= 5:
            break

    reviews_status = get_sentiment(reviews_list)
    movie_reviews = {reviews_list[i]: reviews_status[i]
                     for i in range(len(reviews_list))}
    return movie_reviews


def get_all_details(movie_id, imdb_id):
    info = get_movie_info(movie_id)
    movie_dict = {"tmdb_id": movie_id,
                  "title": info['title'],
                  "image": 'https://image.tmdb.org/t/p/original'+info['backdrop_path'],
                  "overview": info['overview'],
                  "votes": info['vote_average'],
                  "year": info['release_date'].split('-')[0],
                  "reviews": get_reviews_and_sentiment(imdb_id)}
    return movie_dict


app = Flask(__name__, template_folder="templates/")
CORS(app)


@app.route('/')
def home():
    return render_template("index.html", data=list(df['suggestions'].str.capitalize()))


result = False


@app.route('/recommend', methods=['GET', 'POST'])
def get_recommendations():
    title = request.args.get('title')
    title = title.lower()
    print(title)
    if title == None:
        print(title, 'in none')
        return render_template("error.html")
    elif title not in df['suggestions'].unique():
        print(title, 'not in df')
        return render_template("error.html")
    else:
        tmdb_id = (df['tmdb_id'].iloc[df.index[df.suggestions == title]])
        imdb_id = (df['imdb_id'].iloc[df.index[df.suggestions == title]])
        name, year = title.split(
            '(')[0].rstrip(), title.split('(')[1].rstrip(')')
        movie_details = []
        movie_details = get_all_details(
            tmdb_id.to_list()[0], imdb_id.to_list()[0])
        results = recommend.results(title)
        return render_template("movie-info.html", movie_recommendations=results, movie_details=movie_details)


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
