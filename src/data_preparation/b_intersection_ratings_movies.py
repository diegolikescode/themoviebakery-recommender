# script to remove ratings from the movies that didn't existed in the tmdb-movies dataframe
import pandas as pd
import requests

# ratings_df_file = requests.get(
#     'https://bucket-recommender.s3.us-east-1.amazonaws.com/kaggle-ratings.csv')
ratings_df_file = 'https://bucket-recommender.s3.us-east-1.amazonaws.com/kaggle-ratings.csv'

movies_df = pd.read_json('../../data/semi-treated-data/movies_kaggleId.json')
ratings_df = pd.read_csv(ratings_df_file,
                         usecols=['userId', 'movieId', 'rating'])

# ratings_df = pd.read_csv('../../data/raw-data/kaggle-ratings.csv',
#                          usecols=['userId', 'movieId', 'rating'])

movie_kaggle_ids = movies_df['kaggleId'].to_numpy()

new_ratings_df = ratings_df[ratings_df['movieId'].isin(movie_kaggle_ids)]
new_ratings_df.to_csv('../../data/treated-data/all-ratings.csv', index=False)