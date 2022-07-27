# Movie Recommendation system

## INTRODUCTION

Recommender systems are used for providing personalized recommendations based on the user profile and previous behaviour. Recommender systems such as Amazon, Netflix, and YouTube are widely used in the Internet Industry. Recommendation systems help the users to find and select items (e.g., books, movies, restaurants) from the wide collection available on the web or in other electronic information sources. Among a large set of items and a description of the user’s needs, they present to the user a small set of the items that are well suited to the description.
This project focuses on Movie recommendation.
Recommendation algorithms mainly follow following approaches: 

-	**Content-based filtering**: They suggest similar items based on a particular item. This system uses item metadata, such as genre, director, description, actors, etc. for movies, to make these recommendations. 

-	**Collaborative filtering**: user-to-user and item-to-item
This system matches persons with similar interests and provides recommendations based on this matching. 
It does not require item metadata like its content-based counterparts, but requires usres and there respective ratings.

-	**Demographic**: They offer generalized recommendations to every user, based on movie popularity and/or genre. 
The System recommends the same movies to users with similar demographic features. The basic idea behind this system is that movies that are more popular and critically acclaimed will have a higher probability of being liked by the average audience.

-	**Knowledge-based**: It suggests products based on inferences about user’s needs and preferences, item selection and its basis for recommendation.

-	**Hybrid**: It is the one that combines multiple recommendation techniques together to produce the output. If one compares hybrid
recommender systems with collaborative or content-based systems, the recommendation accuracy is usually higher in hybrid system. 

## METHODOLOGY

### Content Based filtering:
This engine computes similarity between movies based on certain metrics and suggests movies that are most similar to a particular movie that a user liked. The metrics used here are:
- Movie Overview.
- Director name, Cast and Genre.

I used the Cosine Similarity to calculate a numeric quantity that denotes the similarity between two movies. Mathematically, it is defined as follows:
 
I have used the TF-IDF Vectorizer, so calculating the Dot Product will directly gives the Cosine Similarity Score. 
Therefore, we will use sklearn's linear_kernel instead of cosine_similarities since it is much faster.

#### Limitations
-	It is not capable of capturing tastes and providing recommendations across genres.
-	It doesn't capture the personal tastes and biases of a user. 
-	Anyone querying our engine for recommendations based on a movie will receive the same recommendations for that movie, regardless of who s/he is.

These limitations are overcame by 

### Collaborative filtering
It is of 2 types:

- **User based filtering**-  This system recommends products to a user that **similar users have liked**. For measuring the similarity between two users we can either use pearson correlation or cosine similarity. 
One main issue is that users’ preference can change over time. It indicates that precomputing the matrix based on their neighboring users may lead to bad performance. To tackle this problem, we can apply item-based CF.

- **Item Based Collaborative Filtering**- This recommends items based on their similarity with the items that the target user rated. 
Likewise, the similarity can be computed with Pearson Correlation or Cosine Similarity.
The major difference is that, in this, we fill in the blank vertically, as oppose to the horizontal manner that user-based CF does.

## DATASET GENREATION:

Scrapping using beautiful soup from imdb website that shows list of films year wise.
To scrape data I used **Beautiful Soup** library in python and passed the url of IMDB website that sorted movies based on of number of votes over years 1991-2022
https://github.com/Aarush2k1/Movie-Recommender/blob/master/datasets-generation/imdb_scraping.ipynb

Collaborative datset: https://www.kaggle.com/rounakbanik/the-movies-dataset?select=ratings_small.csv

Sentiment-analysis dataset: https://www.kaggle.com/datasets/columbine/imdb-dataset-sentiment-analysis-in-csv-format

## ARCHITECTURE

![image](https://user-images.githubusercontent.com/56411093/181216896-3366c2e7-0853-465d-b5dd-c93490da25df.png)
  

## SCREENSHOTS


## Further to-do:
- Automatically add new released movies after week of there release in dataset.
- Create dataset for collborative filtering, i.e need user ratings and movie ratings for the movies for my dataset.
