from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

similarity_df = pd.read_csv("movie_similarity.csv", index_col=0)

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')


@app.route("/recommend", methods=["POST"])
def make_rec():
    if request.method == "POST":
        data = request.json
        movie = data["movie_title"]
        try:
            sim_score = similarity_df[movie]
            sim_movies = sim_score.sort_values(ascending=False)[1:50]
            api_recommendations = sim_movies.index.to_list()
        except:
            api_recommendations = ['Movie not found']
        return {"rec_movie": api_recommendations}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
