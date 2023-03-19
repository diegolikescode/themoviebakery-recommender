# script to remove ratings from the movies that didn't existed in the tmdb-movies dataframe
import pandas as pd

movies_df = pd.read_json('../../data/semi-treated-data/movies_kaggleId.json')
ratings_df = pd.read_csv('../../data/raw-data/kaggle-ratings.csv',
                         usecols=['userId', 'movieId', 'rating'])

movie_kaggle_ids = movies_df['kaggleId'].to_numpy()

new_ratings_df = ratings_df[ratings_df['movieId'].isin(movie_kaggle_ids)]
new_ratings_df.to_csv('../../data/treated-data/all-ratings.csv', index=False)
