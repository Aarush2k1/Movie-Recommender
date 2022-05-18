from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pandas as pd

similarity_df = pd.read_csv("movie_similarity.csv", index_col=0)

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_from_root():
    return render_template("index.html", data=similarity_df.columns.to_list())


@app.route("/recommend", methods=["GET"])
def make_rec():
    if request.method == "GET":
        data = request.args.get('title')
        try:
            sim_score = similarity_df[data]
            sim_movies = sim_score.sort_values(ascending=False)[1:20]
            api_recommendations = sim_movies.index.to_list()
        except:
            api_recommendations = ['Movie not found']
        return {"rec_movie": api_recommendations}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
